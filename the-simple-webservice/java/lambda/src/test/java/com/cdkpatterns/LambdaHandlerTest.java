package com.cdkpatterns;

import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPResponse;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;

import static org.assertj.core.api.Assertions.assertThat;

class LambdaHandlerTest {
    @DisplayName("Test APIGateway handler")
    @Test
    public void testHandleRequest() {
        DynamoDbClient dynamoDbClientMock = Mockito.mock(DynamoDbClient.class);
        APIGatewayV2HTTPEvent input = new APIGatewayV2HTTPEvent();

        LambdaHandler lambdaHandler = new LambdaHandler(dynamoDbClientMock);
        APIGatewayV2HTTPResponse response = lambdaHandler.handleRequest(input, null);

        assertThat(response.getStatusCode()).isEqualTo(200);
        assertThat(response.getBody()).isEqualTo("You have connected with the Lambda");
    }
}