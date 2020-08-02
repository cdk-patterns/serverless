package com.cdkpatterns;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import software.amazon.awssdk.auth.credentials.EnvironmentVariableCredentialsProvider;
import software.amazon.awssdk.core.client.config.ClientOverrideConfiguration;
import software.amazon.awssdk.http.HttpStatusCode;
import software.amazon.awssdk.http.urlconnection.UrlConnectionHttpClient;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.AttributeValue;
import software.amazon.awssdk.services.dynamodb.model.UpdateItemRequest;

import java.util.Map;

public class LambdaHandler implements RequestHandler<APIGatewayV2HTTPEvent, APIGatewayV2HTTPResponse> {
    private static final Logger LOG = LoggerFactory.getLogger(LambdaHandler.class);
    private static final String HITS_TABLE_NAME = System.getenv("HITS_TABLE_NAME");
    private DynamoDbClient dynamoDbClient;

    public LambdaHandler() {
        this(DynamoDbClient.builder()
                .httpClient(UrlConnectionHttpClient.builder().build())
                .region(Region.of(System.getenv("REGION")))
                .credentialsProvider(EnvironmentVariableCredentialsProvider.create())
                .overrideConfiguration(ClientOverrideConfiguration.builder()
                        .build())
                .build());
    }

    public LambdaHandler(DynamoDbClient dynamoDbClient) {
        this.dynamoDbClient = dynamoDbClient;
    }

    @Override
    public APIGatewayV2HTTPResponse handleRequest(APIGatewayV2HTTPEvent event, Context context) {
        LOG.info("Request: {}", event);

        updateHitsCount(event);

        return APIGatewayV2HTTPResponse.builder()
                .withStatusCode(HttpStatusCode.OK)
                .withBody("You have connected with the Lambda")
                .withHeaders(Map.of("Content-Type", "text/html"))
                .build();
    }

    private void updateHitsCount(APIGatewayV2HTTPEvent event) {
        this.dynamoDbClient.updateItem(UpdateItemRequest.builder()
                .tableName(HITS_TABLE_NAME)
                .key(Map.of("path", AttributeValue.builder().s(event.getRawPath()).build()))
                .updateExpression("ADD hits :incr")
                .expressionAttributeValues(Map.of(":incr", AttributeValue.builder().n("1").build()))
                .build());
    }
}