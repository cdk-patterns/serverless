package com.cdkpatterns;

import java.util.Map;

import software.amazon.awscdk.core.CfnOutput;
import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.core.StackProps;
import software.amazon.awscdk.services.lambda.Function;
import software.amazon.awscdk.services.lambda.Code;
import software.amazon.awscdk.services.lambda.Runtime;
import software.amazon.awscdk.services.sam.CfnApplication;
import software.amazon.awscdk.services.sam.CfnApplication.ApplicationLocationProperty;

public class TheLambdaPowerTunerStack extends Stack {
    public TheLambdaPowerTunerStack(final Construct scope, final String id) {
        this(scope, id, null);
    }
    
    private String powerValues = "128,256,512,1024,1536,3008";
    private String lambdaResource = "*";

    public TheLambdaPowerTunerStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        
        //  An example lambda that can be used to test the powertuner
        Function functionExample = Function.Builder.create(this, "exampleLambda")
        		.runtime(Runtime.NODEJS_12_X)
        		.handler("index.handler")
        		.code(Code.fromInline("exports.handler = function(event, ctx, cb) { return cb(null, 'hi'); }"))
        		.build();
        
        // uncomment to only allow this power tuner to manipulate this defined function
        // String lambdaResource = functionExample.getFunctionArn();

        // Output the Lambda function ARN in the deploy logs to ease testing
        CfnOutput.Builder.create(this, "LambdaARN")
        	.value(functionExample.getFunctionArn())
        	.build();
        
        // Deploy the aws-lambda-powertuning application from the Serverless Application Repository
        // https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:451282441545:applications~aws-lambda-power-tuning
        CfnApplication.Builder.create(this, "powerTuner")
        .location(new ApplicationLocationProperty
        		.Builder()
        		.applicationId("arn:aws:serverlessrepo:us-east-1:451282441545:applications/aws-lambda-power-tuning")
        		.semanticVersion("3.4.0")
        		.build())
        .parameters(Map.of(
        		"lambdaResource", lambdaResource,
        		"PowerValues", powerValues
        		))
        .build();
        
    }
}
