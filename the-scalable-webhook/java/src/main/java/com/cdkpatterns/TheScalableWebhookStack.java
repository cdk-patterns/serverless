package com.cdkpatterns;

import java.util.Map;

import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.Duration;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.core.StackProps;
import software.amazon.awscdk.services.dynamodb.Table;
import software.amazon.awscdk.services.dynamodb.Attribute;
import software.amazon.awscdk.services.dynamodb.AttributeType;
import software.amazon.awscdk.services.lambda.Function;
import software.amazon.awscdk.services.lambda.Code;
import software.amazon.awscdk.services.lambda.Runtime;
import software.amazon.awscdk.services.lambda.eventsources.SqsEventSource;
import software.amazon.awscdk.services.sqs.Queue;
import software.amazon.awscdk.services.apigateway.LambdaRestApi;

public class TheScalableWebhookStack extends Stack {
    public TheScalableWebhookStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public TheScalableWebhookStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        /*
         * DynamoDB Table
         * This is standing in for what is RDS on the diagram due to simpler/cheaper setup
         */
        Table dynamoDbTable = Table.Builder.create(this, "Messages")
        		.partitionKey(Attribute.builder()
        				.name("id")
        				.type(AttributeType.STRING)
        				.build())
        		.build();
        		
        /*
         * Queue Setup
         */
        Queue queueRds = Queue.Builder.create(this, "RDSPublishQueue")
        		.visibilityTimeout(Duration.seconds(300))
        		.build();
        
        /*
         * Lambdas
         * Both publisher and subscriber from pattern
         * 
         * defines an AWS  Lambda resource to publish to our sqs_queue
         */
        Function functionPublish = Function.Builder.create(this, "SQSPublishLambdaHandler")
        		.runtime(Runtime.NODEJS_12_X) // execution environment
        		.handler("lambda.handler") // file is "lambda", function is "handler"
        		.code(Code.fromAsset("lambda_fns/publish")) // code loaded from the "lambda_fns/publish" directory
        		.environment(Map.of(
        				"queueURL", queueRds.getQueueUrl()
        				))
        		.build();
        
        queueRds.grantSendMessages(functionPublish);
        
        /*
         * defines an AWS  Lambda resource to pull from our sqs_queue
         */
        
        Function functionSubscribe = Function.Builder.create(this, "SQSSubscribeLambdaHandler")
        		.runtime(Runtime.NODEJS_12_X) // execution environment
        		.handler("lambda.handler") // file is "lambda", function is "handler"
        		.code(Code.fromAsset("lambda_fns/subscribe")) // code loaded from the "lambda_fns/subscribe" directory
        		.environment(Map.of(
        				"queueURL", queueRds.getQueueUrl(),
        				"tableName", dynamoDbTable.getTableName()
        				))
        		.reservedConcurrentExecutions(2) // throttle lambda to 2 concurrent invocations
        		.build();
        
        queueRds.grantConsumeMessages(functionSubscribe);
        functionSubscribe.addEventSource(new SqsEventSource(queueRds));
        dynamoDbTable.grantReadWriteData(functionSubscribe);
        
        /*
         * defines an API Gateway REST API resource backed by our "sqs_publish_lambda" function.
         */
        LambdaRestApi.Builder.create(this, "Endpoint").handler(functionPublish).build();

        
    }
}
