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
     * DynamoDB Table
     * 
     * We store Flight, Hotel and Rental Car bookings in the same table.
     * 
     * For more help with single table DB structures see - https://www.dynamodbbook.com/
     * 
     * pk - the trip_id e.g. 1234
     * sk - bookingtype#booking_id e.g. HOTEL#345634, FLIGHT#574576, PAYMENT#45245
     */

    const bookingsTable = new dynamodb.Table(this, 'Bookings', {
      partitionKey: { name: 'pk', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'sk', type: dynamodb.AttributeType.STRING }
    });

    /**
     * Lambda Functions
     * 
     * We need Booking and Cancellation functions for our 3 services
     * All functions need access to our DynamoDB table above.
     * 
     * We also need to take payment for this trip
     * 
     * 1) Flights
     * 2) Hotel
     * 3) Payment
     */

    // 1) Flights 
    let reserveFlightLambda = this.createLambda(this, 'reserveFlightLambdaHandler', 'flights/reserveFlight.handler', bookingsTable);
    let confirmFlightLambda = this.createLambda(this, 'confirmFlightLambdaHandler', 'flights/confirmFlight.handler', bookingsTable);
    let cancelFlightLambda = this.createLambda(this, 'cancelFlightLambdaHandler', 'flights/cancelFlight.handler', bookingsTable);

    // 2) Hotel 
    let reserveHotelLambda = this.createLambda(this, 'reserveHotelLambdaHandler', 'hotel/reserveHotel.handler', bookingsTable);
    let confirmHotellambda = this.createLambda(this, 'confirmHotelLambdaHandler', 'hotel/confirmHotel.handler', bookingsTable);
    let cancelHotelLambda = this.createLambda(this, 'cancelHotelLambdaHandler', 'hotel/cancelHotel.handler', bookingsTable);

    // 3) Payment For Holiday
    let takePaymentLambda = this.createLambda(this, 'takePaymentLambdaHandler', 'payment/takePayment.handler', bookingsTable);
    let refundPaymentLambda = this.createLambda(this, 'refundPaymentLambdaHandler', 'payment/refundPayment.handler', bookingsTable);

    /**
     * Saga Pattern Stepfunction
     * 
     * Follows a strict order:
     * 1) Reserve Flights and Hotel
     * 2) Take Payment
     * 3) Confirm Flight and Hotel booking
     */

    // Our two end states
    const bookingFailed = new sfn.Fail(this, "Sorry, We Couldn't make the booking", {});
    const bookingSucceeded = new sfn.Succeed(this, 'We have made your booking!');


    /**
     * 1) Reserve Flights and Hotel
     */
    const cancelHotelReservation = new sfn.Task(this, 'CancelHotelReservation', {
      task: new tasks.RunLambdaTask(cancelHotelLambda),
      resultPath: '$.CancelHotelReservationResult',
    }).addRetry({maxAttempts:3}) // retry this task a max of 3 times if it fails
    .next(bookingFailed);

    const reserveHotel = new sfn.Task(this, 'ReserveHotel', {
      task: new tasks.RunLambdaTask(reserveHotelLambda),
      resultPath: '$.ReserveHotelResult',
    }).addCatch(cancelHotelReservation, {
      resultPath: "$.ReserveHotelError"
    });

    const cancelFlightReservation = new sfn.Task(this, 'CancelFlightReservation', {
      task: new tasks.RunLambdaTask(cancelFlightLambda),
      resultPath: '$.CancelFlightReservationResult',
    }).addRetry({maxAttempts:3}) // retry this task a max of 3 times if it fails
    .next(cancelHotelReservation);

    const reserveFlight = new sfn.Task(this, 'ReserveFlight', {
      task: new tasks.RunLambdaTask(reserveFlightLambda),
      resultPath: '$.ReserveFlightResult',
    }).addCatch(cancelFlightReservation, {
      resultPath: "$.ReserveFlightError"
    });

    /**
     * 2) Take Payment
     */
    const refundPayment = new sfn.Task(this, 'RefundPayment', {
      task: new tasks.RunLambdaTask(refundPaymentLambda),
      resultPath: '$.RefundPaymentResult',
    }).addRetry({maxAttempts:3}) // retry this task a max of 3 times if it fails
    .next(cancelFlightReservation);

    const takePayment = new sfn.Task(this, 'TakePayment', {
      task: new tasks.RunLambdaTask(takePaymentLambda),
      resultPath: '$.TakePaymentResult',
    }).addCatch(refundPayment, {
      resultPath: "$.TakePaymentError"
    });

    /**
     * 3) Confirm Flight and Hotel booking
     */
    const confirmHotelBooking = new sfn.Task(this, 'ConfirmHotelBooking', {
      task: new tasks.RunLambdaTask(confirmHotellambda),
      resultPath: '$.ConfirmHotelBookingResult',
    }).addCatch(refundPayment, {
      resultPath: "$.ConfirmHotelBookingError"
    });

    const confirmFlight = new sfn.Task(this, 'ConfirmFlight', {
      task: new tasks.RunLambdaTask(confirmFlightLambda),
      resultPath: '$.ConfirmFlightResult',
    }).addCatch(refundPayment, {
      resultPath: "$.ConfirmFlightError"
    });

    //Step function definition
    const definition = sfn.Chain
    .start(reserveHotel)
    .next(reserveFlight)
    .next(takePayment)
    .next(confirmHotelBooking)
    .next(confirmFlight)
    .next(bookingSucceeded)

    let saga = new sfn.StateMachine(this, 'BookingSaga', {
      definition,
      timeout: cdk.Duration.minutes(5)
    });

    // defines an AWS Lambda resource to connect to our API Gateway and kick
    // off our step function
    const sagaLambda = new lambda.Function(this, 'sagaLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns'),
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
      code: lambda.Code.fromAsset('lambda-fns'),
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
