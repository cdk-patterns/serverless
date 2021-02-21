package com.cdkpatterns;

import java.util.List;

import software.amazon.awscdk.core.CfnOutput;
import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.core.StackProps;
import software.amazon.awscdk.services.lambda.Function;
import software.amazon.awscdk.services.lambda.Runtime;
import software.amazon.awscdk.services.lambda.Code;
import software.amazon.awscdk.services.iam.PolicyStatement;
import software.amazon.awscdk.services.iam.PolicyStatementProps;
import software.amazon.awscdk.services.iam.Effect;
import software.amazon.awscdk.services.apigatewayv2.HttpApi;
import software.amazon.awscdk.services.apigatewayv2.integrations.LambdaProxyIntegration;
import software.amazon.awscdk.services.apigatewayv2.integrations.LambdaProxyIntegrationProps;


public class PollyStack extends Stack {
    public PollyStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public PollyStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        // Lambda Function that takes in text and returns a polly voice synthesis
        Function pollyFunction = Function.Builder.create(this, "pollyHandler")
        		.runtime(Runtime.PYTHON_3_8)
        		.code(Code.fromAsset("lambda_fns"))
        		.handler("polly.handler")
        		.build();
        
        // https://docs.aws.amazon.com/polly/latest/dg/api-permissions-reference.html
        // https://docs.aws.amazon.com/translate/latest/dg/translate-api-permissions-ref.html
        PolicyStatement pollyPolicy = new PolicyStatement(
        		new PolicyStatementProps
        		.Builder()
        		.effect(Effect.ALLOW)
        		.resources(List.of("*"))
        		.actions(List.of("translate:TranslateText", "polly:SynthesizeSpeech"))
        		.build());
        
        pollyFunction.addToRolePolicy(pollyPolicy);
        
        // defines an API Gateway Http API resource backed by our "pollyHandler" function.
        HttpApi httpApi = HttpApi.Builder.create(this, "Polly")
        		.defaultIntegration(
        				new LambdaProxyIntegration(
        						new LambdaProxyIntegrationProps
        						.Builder()
        						.handler(pollyFunction)
        						.build()
        						))
        		.build();
        
        CfnOutput.Builder.create(this, "HTTP API Url")
        	.value(httpApi.getUrl())
        	.build();
        
    }
}
