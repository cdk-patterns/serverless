import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import apigw = require('@aws-cdk/aws-apigateway');
import sfn = require('@aws-cdk/aws-stepfunctions');
import tasks = require('@aws-cdk/aws-stepfunctions-tasks');

export class TheSagaStepfunctionSingleTableStack extends cdk.Stack {

  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * DynamoDB Tables
     * 
     * We store Flight, Hotel and Rental Car bookings in the same table.
     * 
     * pk - the trip_id e.g. 1234
     * sk - bookingtype#booking_id e.g. HOTEL#345634, FLIGHT#574576, RENTAL#45245
     */

    const bookingsTable = new dynamodb.Table(this, 'Bookings', {
      partitionKey: { name: 'pk', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'sk', type: dynamodb.AttributeType.STRING }
    });

    /**
     * Lambda Functions
     * 
     * We need Booking and Cancellation functions for our 3 services
     * All functions need access to our DynamoDB table above
     * 
     * 1) Flights
     * 2) Hotel
     * 3) Rental Car
     */

    // 1) Flights 
    let bookFlightLambda = this.createLambda(this, 'bookFlightLambdaHandler', 'bookFlight.handler', bookingsTable);
    let cancelFlightLambda = this.createLambda(this, 'cancelFlightLambdaHandler', 'cancelFlight.handler', bookingsTable);

    // 2) Hotel 
    let reserveHotelLambda = this.createLambda(this, 'reserveHotelLambdaHandler', 'reserveHotel.handler', bookingsTable);
    let confirmHotellambda = this.createLambda(this, 'confirmHotelLambdaHandler', 'confirmHotel.handler', bookingsTable);
    let cancelHotelLambda = this.createLambda(this, 'cancelHotelLambdaHandler', 'cancelHotel.handler', bookingsTable);

    // 3) Rental Car 
    let bookRentalLambda = this.createLambda(this, 'bookRentalLambdaHandler', 'bookRental.handler', bookingsTable);
    let cancelRentalLambda = this.createLambda(this, 'cancelRentalLambdaHandler', 'cancelRental.handler', bookingsTable);

    // 4) Payment For Holiday
    let takePaymentLambda = this.createLambda(this, 'takePaymentLambdaHandler', 'takePayment.handler', bookingsTable);
    let refundPaymentLambda = this.createLambda(this, 'refundPaymentLambdaHandler', 'refundPayment.handler', bookingsTable);

    /**
     * Saga Pattern Stepfunction
     */

    // Our two end states
    const bookingFailed = new sfn.Fail(this, "Sorry, We Couldn't make the booking", {});
    const bookingSucceeded = new sfn.Succeed(this, 'We have made your booking!');


    // Hotel
    const cancelHotelReservation = new sfn.Task(this, 'CancelHotelReservation', {
      task: new tasks.InvokeFunction(cancelHotelLambda),
      resultPath: '$.CancelHotelReservationResult',
    }).addRetry({maxAttempts:3}) // retry this task a max of 3 times if it fails
    .next(bookingFailed);

    const reserveHotel = new sfn.Task(this, 'ReserveHotel', {
      task: new tasks.InvokeFunction(reserveHotelLambda),
      resultPath: '$.ReserveHotelResult',
    }).addCatch(cancelHotelReservation, {
      resultPath: "$.ReserveHotelError"
    });

    // Payment
    const refundPayment = new sfn.Task(this, 'RefundPayment', {
      task: new tasks.InvokeFunction(refundPaymentLambda),
      resultPath: '$.RefundPaymentResult',
    }).addCatch(cancelHotelReservation, {
      resultPath: "$.RefundPaymentError"
    })
    .next(cancelHotelReservation);

    const takePayment = new sfn.Task(this, 'TakePayment', {
      task: new tasks.InvokeFunction(takePaymentLambda),
      resultPath: '$.TakePaymentResult',
    }).addCatch(refundPayment, {
      resultPath: "$.TakePaymentError"
    });

    const confirmHotelBooking = new sfn.Task(this, 'ConfirmHotelBooking', {
      task: new tasks.InvokeFunction(confirmHotellambda),
      resultPath: '$.ConfirmHotelBookingResult',
    }).addCatch(refundPayment, {
      resultPath: "$.ConfirmHotelBookingError"
    });

    


    // Flights
    /*const cancelFlight = new sfn.Task(this, 'CancelFlight', {
      task: new tasks.InvokeFunction(cancelFlightLambda),
      resultPath: '$.CancelFlightResult',
    }).addRetry({maxAttempts:3}) // retry this task a max of 3 times if it fails
    .next(cancelHotel);

    const bookFlight = new sfn.Task(this, 'BookFlight', {
      task: new tasks.InvokeFunction(bookFlightLambda),
      resultPath: '$.BookFlightResult',
    }).addCatch(cancelFlight, {
      resultPath: "$.CancelFlightError"
    });

    // Rental Car
    const cancelRental = new sfn.Task(this, 'CancelRental', {
      task: new tasks.InvokeFunction(cancelRentalLambda),
      resultPath: '$.CancelRentalResult',
    }).addRetry({maxAttempts:3}) // retry this task a max of 3 times if it fails
    .next(cancelFlight);

    const bookRental = new sfn.Task(this, 'BookRental', {
      task: new tasks.InvokeFunction(bookRentalLambda),
      resultPath: '$.BookRentalResult',
    }).addCatch(cancelRental, {
      resultPath: "$.CancelRentalError"
    });*/

    //Step function definition
    const definition = sfn.Chain
    .start(reserveHotel)
    .next(takePayment)
    .next(confirmHotelBooking)
    .next(bookingSucceeded)

    let saga = new sfn.StateMachine(this, 'BookingSaga', {
      definition,
      timeout: cdk.Duration.minutes(5)
    });

    // defines an AWS Lambda resource to connect to our API Gateway and kick
    // off our step function
    const sagaLambda = new lambda.Function(this, 'sagaLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'sagaLambda.handler',
      environment: {
        statemachine_arn: saga.stateMachineArn
      }
    });

    saga.grantStartExecution(sagaLambda);

    /**
     * Simple API Gateway proxy integration
     */
    // defines an API Gateway REST API resource backed by our "stateMachineLambda" function.
    new apigw.LambdaRestApi(this, 'SagaPatternSingleTable', {
      handler: sagaLambda
    });
  }

  /**
   * Helper function to shorten Lambda boilerplate as we have 6 in this stack
   * @param scope 
   * @param id 
   * @param handler 
   * @param table 
   */
  createLambda(scope:cdk.Stack, id:string, handler:string, table:dynamodb.Table){
    
    // Create a Node Lambda with the table name passed in as an environment variable
    let fn =  new lambda.Function(scope, id, {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas/singleTable'),
      handler:handler,
      environment: {
        TABLE_NAME: table.tableName
      }
    });
    // Give our Lambda permissions to read and write data from the passed in DynamoDB table
    table.grantReadWriteData(fn);

    return fn;
  }
}
