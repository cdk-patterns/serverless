package com.cdkpatterns;

import java.util.Map;

import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.RemovalPolicy;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.core.StackProps;
import software.amazon.awscdk.services.dynamodb.Table;
import software.amazon.awscdk.services.dynamodb.Attribute;
import software.amazon.awscdk.services.dynamodb.AttributeType;
import software.amazon.awscdk.services.lambda.Function;
import software.amazon.awscdk.services.lambda.Code;
import software.amazon.awscdk.services.lambda.Runtime;
import software.amazon.awscdk.services.events.Rule;
import software.amazon.awscdk.services.events.Schedule;
import software.amazon.awscdk.services.events.targets.LambdaFunction;

public class TheScheduledLambdaStack extends Stack {
    public TheScheduledLambdaStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public TheScheduledLambdaStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        // DynamoDB Table
        Table dynamoDbTable = Table.Builder.create(this, "RequestTable")
        		.partitionKey(Attribute.builder()
        				.name("requestid")
        				.type(AttributeType.STRING)
        				.build())
        		.removalPolicy(RemovalPolicy.DESTROY)
        		.build();
        
        // Create the Lambda function we want to run on a schedule
        Function functionScheduled = Function.Builder.create(this, "ScheduledLambda")
        		.runtime(Runtime.NODEJS_12_X) // execution environment
        		.handler("index.handler") // file is "index", function is "handler"
        		.code(Code.fromAsset("lambda_fns")) // code loaded from the "lambda_fns" directory
        		.environment(Map.of(
        				"TABLE_NAME", dynamoDbTable.getTableName()
        				))
        		.build();
        
        // Allow our lambda fn to write to the table
        dynamoDbTable.grantReadWriteData(functionScheduled);
        
        // Create EventBridge rule that will execute our Lambda every 2 minutes
        Rule ruleScheduled = Rule.Builder.create(this, "scheduledLambda-schedule")
        		.schedule(Schedule.expression("rate(2 minutes)"))
        		.build();
        
        // Set the target of our EventBridge rule to our Lambda function
        ruleScheduled.addTarget(new LambdaFunction(functionScheduled));
        
    }
}
