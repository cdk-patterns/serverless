from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as api_gw,
    aws_dynamodb as dynamo_db,
    core
)


class TheSagaStepfunctionStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ###
        # DynamoDB Table
        ###
        # We store Flight, Hotel and Rental Car bookings in the same table.
        #
        # For more help with single table DB structures see - https://www.dynamodbbook.com/
        # pk - the trip_id e.g. 1234
        # sk - bookingtype#booking_id e.g. HOTEL#345634, FLIGHT#574576, PAYMENT#45245
        table = dynamo_db.Table(self, "Bookings",
                                partition_key=dynamo_db.Attribute(name="pk", type=dynamo_db.AttributeType.STRING),
                                sort_key=dynamo_db.Attribute(name="sk", type=dynamo_db.AttributeType.STRING)
                                )

        ###
        # Lambda Functions
        ###
        # We need Booking and Cancellation functions for our 3 services
        #
        # All functions need access to our DynamoDB table above.
        # We also need to take payment for this trip
        #
        # 1) Flights
        # 2) Hotel
        # 3) Payment

        # 1) Flights
        reserve_flight_lambda = self.create_lambda(scope=self, lambda_id="reserveFlightLambdaHandler",
                                                   handler='flights/reserveFlight.handler', table=table)
        confirm_flight_lambda = self.create_lambda(scope=self, lambda_id="confirmFlightLambdaHandler",
                                                   handler='flights/confirmFlight.handler', table=table)
        cancel_flight_lambda = self.create_lambda(scope=self, lambda_id="cancelFlightLambdaHandler",
                                                  handler='flights/cancelFlight.handler', table=table)

        # 2) Hotel
        reserve_hotel_lambda = self.create_lambda(scope=self, lambda_id="reserveHotelLambdaHandler",
                                                  handler='hotel/reserveHotel.handler', table=table)
        confirm_hotel_lambda = self.create_lambda(scope=self, lambda_id="confirmHotelLambdaHandler",
                                                  handler='hotel/confirmHotel.handler', table=table)
        cancel_hotel_lambda = self.create_lambda(scope=self, lambda_id="cancelHotelLambdaHandler",
                                                 handler='hotel/cancelHotel.handler', table=table)

        # 3) Payment For Holiday
        take_payment_lambda = self.create_lambda(scope=self, lambda_id="takePaymentLambdaHandler",
                                                 handler='payment/takePayment.handler', table=table)
        refund_payment_lambda = self.create_lambda(scope=self, lambda_id="refundPaymentLambdaHandler",
                                                   handler='payment/refundPayment.handler', table=table)

    def create_lambda(self, scope: core.Stack, lambda_id: str, handler: str, table: dynamo_db.Table):
        fn = _lambda.Function(scope, lambda_id,
                              runtime=_lambda.Runtime.NODEJS_12_X,
                              handler=handler,
                              code=_lambda.Code.from_asset("lambdas"),
                              environment={
                                  'TABLE_NAME': table.table_name
                              }
                              )
        table.grant_read_write_data(fn)
        return fn
