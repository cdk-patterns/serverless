import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');

export class TheSagaStepfunctionStack extends cdk.Stack {

  /**
   * Helper function to shorten Lambda boilerplate as we have 6 in this stack
   * @param scope 
   * @param id 
   * @param handler 
   * @param tablename 
   */
  createLambdaFunction(scope:cdk.Stack, id:string, handler:string, tablename:string){
    return new lambda.Function(scope, id, {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler:handler,
      environment: {
        TABLE_NAME: tablename
      }
    });
  }

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

    // Booking
    let bookFlightLambda = this.createLambdaFunction(this, 'bookFlightLambdaHandler', 'bookFlight.handler', flightBookingsTable.tableName);
    flightBookingsTable.grantReadWriteData(bookFlightLambda)

    // Cancellation
    let cancelFlightLambda = this.createLambdaFunction(this, 'cancelFlightLambdaHandler', 'cancelFlight.handler', flightBookingsTable.tableName);
    flightBookingsTable.grantReadWriteData(cancelFlightLambda)

    // 2) Hotel 

    // Booking
    let bookHotelLambda = this.createLambdaFunction(this, 'bookHotelLambdaHandler', 'bookHotel.handler', hotelBookingsTable.tableName);
    hotelBookingsTable.grantReadWriteData(bookHotelLambda)

    // Cancellation
    let cancelHotelLambda = this.createLambdaFunction(this, 'cancelHotelLambdaHandler', 'cancelHotel.handler', hotelBookingsTable.tableName);
    hotelBookingsTable.grantReadWriteData(cancelHotelLambda)

    // 3) Rental Car 

    // Booking
    let bookRentalLambda = this.createLambdaFunction(this, 'bookRentalLambdaHandler', 'bookRental.handler', rentalBookingsTable.tableName);
    rentalBookingsTable.grantReadWriteData(bookRentalLambda)

    // Cancellation
    let cancelRentalLambda = this.createLambdaFunction(this, 'cancelRentalLambdaHandler', 'cancelRental.handler', rentalBookingsTable.tableName);
    rentalBookingsTable.grantReadWriteData(cancelRentalLambda)
  }
}
