import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import apigw = require('@aws-cdk/aws-apigateway');
import sfn = require('@aws-cdk/aws-stepfunctions');
import tasks = require('@aws-cdk/aws-stepfunctions-tasks');

export class TheSagaStepfunctionStack extends cdk.Stack {

  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * DynamoDB Tables
     * 
     * We store Flight, Hotel and Rental Car bookings in separate tables
     */

    const flightBookingsTable = new dynamodb.Table(this, 'FlightBookings', {
      partitionKey: { name: 'trip_id', type: dynamodb.AttributeType.STRING }
    });

    const hotelBookingsTable = new dynamodb.Table(this, 'HotelBookings', {
      partitionKey: { name: 'trip_id', type: dynamodb.AttributeType.STRING }
    });

    const rentalBookingsTable = new dynamodb.Table(this, 'RentalBookings', {
      partitionKey: { name: 'trip_id', type: dynamodb.AttributeType.STRING }
    });

    /**
     * Lambda Functions
     * 
     * We need Booking and Cancellation functions for our 3 services
     * All functions need access to one of the DynamoDB tables above
     * 
     * 1) Flights
     * 2) Hotel
     * 3) Rental Car
     */

    // 1) Flights 
    let bookFlightLambda = this.createLambda(this, 'bookFlightLambdaHandler', 'bookFlight.handler', flightBookingsTable);
    let cancelFlightLambda = this.createLambda(this, 'cancelFlightLambdaHandler', 'cancelFlight.handler', flightBookingsTable);

    // 2) Hotel 
    let bookHotelLambda = this.createLambda(this, 'bookHotelLambdaHandler', 'bookHotel.handler', hotelBookingsTable);
    let cancelHotelLambda = this.createLambda(this, 'cancelHotelLambdaHandler', 'cancelHotel.handler', hotelBookingsTable);

    // 3) Rental Car 
    let bookRentalLambda = this.createLambda(this, 'bookRentalLambdaHandler', 'bookRental.handler', rentalBookingsTable);
    let cancelRentalLambda = this.createLambda(this, 'cancelRentalLambdaHandler', 'cancelRental.handler', rentalBookingsTable);

    /**
     * Saga Pattern Stepfunction
     */

    // Our two end states
    const bookingFailed = new sfn.Fail(this, "Sorry, We Couldn't make the booking", {});
    const bookingSucceeded = new sfn.Succeed(this, 'We have made your booking!');

    // Hotel
    const cancelHotel = new sfn.Task(this, 'CancelHotel', {
      task: new tasks.InvokeFunction(cancelHotelLambda),
      resultPath: '$.CancelHotelResult',
    }).addRetry({maxAttempts:3}) // retry this task a max of 3 times if it fails
    .next(bookingFailed);

    const bookHotel = new sfn.Task(this, 'BookHotel', {
      task: new tasks.InvokeFunction(bookHotelLambda),
      resultPath: '$.BookHotelResult',
    }).addCatch(cancelHotel, {
      resultPath: "$.BookHotelError"
    });


    // Flights
    const cancelFlight = new sfn.Task(this, 'CancelFlight', {
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
    });

    //Step function definition
    const definition = sfn.Chain
    .start(bookHotel)
    .next(bookFlight)
    .next(bookRental)
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
    new apigw.LambdaRestApi(this, 'SagaPattern', {
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
      code: lambda.Code.asset('lambdas'),
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
