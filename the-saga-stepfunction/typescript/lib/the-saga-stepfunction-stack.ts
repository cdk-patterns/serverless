import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');

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

    // Flight Booking
    let bookFlightLambda = new lambda.Function(this, 'bookFlightLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'bookFlight.handler',
      environment: {
        TABLE_NAME: flightBookingsTable.tableName
      }
    });
    flightBookingsTable.grantReadWriteData(bookFlightLambda)

    // Flight Cancellation
    let cancelFlightLambda = new lambda.Function(this, 'cancelFlightLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'cancelFlight.handler',
      environment: {
        TABLE_NAME: flightBookingsTable.tableName
      }
    });
    flightBookingsTable.grantReadWriteData(cancelFlightLambda)

    // 2) Hotel 

    // Hotel Booking
    let bookHotelLambda = new lambda.Function(this, 'bookHotelLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'bookHotel.handler',
      environment: {
        TABLE_NAME: hotelBookingsTable.tableName
      }
    });
    hotelBookingsTable.grantReadWriteData(bookHotelLambda)

    // Hotel Cancellation
    let cancelHotelLambda = new lambda.Function(this, 'cancelHotelLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'cancelHotel.handler',
      environment: {
        TABLE_NAME: hotelBookingsTable.tableName
      }
    });
    hotelBookingsTable.grantReadWriteData(cancelHotelLambda)

    // 3) Rental Car 

    // Rental Car Booking
    let bookRentalLambda = new lambda.Function(this, 'bookRentalLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'bookRental.handler',
      environment: {
        TABLE_NAME: rentalBookingsTable.tableName
      }
    });
    rentalBookingsTable.grantReadWriteData(bookRentalLambda)

    // Rental Car Cancellation
    let cancelRentalLambda = new lambda.Function(this, 'cancelRentalLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'cancelRental.handler',
      environment: {
        TABLE_NAME: rentalBookingsTable.tableName
      }
    });
    rentalBookingsTable.grantReadWriteData(cancelRentalLambda)
  }
}
