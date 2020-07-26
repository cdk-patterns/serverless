from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as api_gw,
    aws_dynamodb as dynamo_db,
    aws_stepfunctions as step_fn,
    aws_stepfunctions_tasks as step_fn_tasks,
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

        ###
        # Saga Pattern Step Function
        ###
        # Follows a strict order:
        # 1) Reserve Flights and Hotel
        # 2) Take Payment
        # 3) Confirm Flight and Hotel booking

        # Our two end states
        booking_succeeded = step_fn.Succeed(self, 'We have made your booking!')
        booking_failed = step_fn.Fail(self, "Sorry, We Couldn't make the booking")

        # 1) Reserve Flights and Hotel
        cancel_hotel_reservation = step_fn.Task(self, 'CancelHotelReservation',
                                                task=step_fn_tasks.RunLambdaTask(cancel_hotel_lambda),
                                                result_path='$.CancelHotelReservationResult'
                                                ).add_retry(max_attempts=3).next(booking_failed)

        reserve_hotel = step_fn.Task(self, 'ReserveHotel',
                                     task=step_fn_tasks.RunLambdaTask(reserve_hotel_lambda),
                                     result_path='$.ReserveHotelResult'
                                     ).add_catch(cancel_hotel_reservation, result_path="$.ReserveHotelError")

        cancel_flight_reservation = step_fn.Task(self, 'CancelFlightReservation',
                                                 task=step_fn_tasks.RunLambdaTask(cancel_flight_lambda),
                                                 result_path='$.CancelFlightReservationResult'
                                                 ).add_retry(max_attempts=3).next(cancel_hotel_reservation)

        reserve_flight = step_fn.Task(self, 'ReserveFlight',
                                      task=step_fn_tasks.RunLambdaTask(reserve_flight_lambda),
                                      result_path='$.ReserveFlightResult'
                                      ).add_catch(cancel_flight_reservation, result_path="$.ReserveFlightError")

        # 2) Take Payment
        refund_payment = step_fn.Task(self, 'RefundPayment',
                                      task=step_fn_tasks.RunLambdaTask(refund_payment_lambda),
                                      result_path='$.RefundPaymentResult'
                                      ).add_retry(max_attempts=3).next(cancel_flight_reservation)

        take_payment = step_fn.Task(self, 'TakePayment',
                                    task=step_fn_tasks.RunLambdaTask(take_payment_lambda),
                                    result_path='$.TakePaymentResult'
                                    ).add_catch(refund_payment, result_path="$.TakePaymentError")

        # 3) Confirm Flight and Hotel Booking
        confirm_hotel = step_fn.Task(self, 'ConfirmHotelBooking',
                                     task=step_fn_tasks.RunLambdaTask(confirm_hotel_lambda),
                                     result_path='$.ConfirmHotelBookingResult'
                                     ).add_catch(refund_payment, result_path="$.ConfirmHotelBookingError")

        confirm_flight = step_fn.Task(self, 'ConfirmFlight',
                                      task=step_fn_tasks.RunLambdaTask(confirm_flight_lambda),
                                      result_path='$.ConfirmFlightResult'
                                      ).add_catch(refund_payment, result_path="$.ConfirmFlightError")

        definition = step_fn.Chain \
            .start(reserve_hotel) \
            .next(reserve_flight) \
            .next(take_payment) \
            .next(confirm_hotel) \
            .next(confirm_flight) \
            .next(booking_succeeded)

        saga = step_fn.StateMachine(self, 'BookingSaga', definition=definition, timeout=core.Duration.minutes(5))

        # defines an AWS Lambda resource to connect to our API Gateway and kick
        # off our step function
        saga_lambda = _lambda.Function(self, "sagaLambdaHandler",
                                       runtime=_lambda.Runtime.NODEJS_12_X,
                                       handler="sagaLambda.handler",
                                       code=_lambda.Code.from_asset("lambda_fns"),
                                       environment={
                                           'statemachine_arn': saga.state_machine_arn
                                       }
                                       )
        saga.grant_start_execution(saga_lambda)

        # defines an API Gateway REST API resource backed by our "stateMachineLambda" function.
        api_gw.LambdaRestApi(self, 'SagaPatternSingleTable',
                             handler=saga_lambda
                             )

    def create_lambda(self, scope: core.Stack, lambda_id: str, handler: str, table: dynamo_db.Table):
        fn = _lambda.Function(scope, lambda_id,
                              runtime=_lambda.Runtime.NODEJS_12_X,
                              handler=handler,
                              code=_lambda.Code.from_asset("lambda_fns"),
                              environment={
                                  'TABLE_NAME': table.table_name
                              }
                              )
        table.grant_read_write_data(fn)
        return fn
