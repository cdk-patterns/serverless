package com.cdkpatterns;


import java.util.List;
import java.util.Map;

import software.amazon.awscdk.core.CfnOutput;
import software.amazon.awscdk.core.CfnOutputProps;
import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.Duration;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.core.StackProps;
import software.amazon.awscdk.services.apigatewayv2.CfnIntegration;
import software.amazon.awscdk.services.apigatewayv2.CfnIntegrationProps;
import software.amazon.awscdk.services.apigatewayv2.CfnRoute;
import software.amazon.awscdk.services.apigatewayv2.CfnRouteProps;
import software.amazon.awscdk.services.apigatewayv2.HttpApi;
import software.amazon.awscdk.services.apigatewayv2.HttpApiProps;
import software.amazon.awscdk.services.apigatewayv2.HttpRouteKey;
import software.amazon.awscdk.services.iam.Effect;
import software.amazon.awscdk.services.iam.PolicyDocument;
import software.amazon.awscdk.services.iam.PolicyDocumentProps;
import software.amazon.awscdk.services.iam.PolicyStatement;
import software.amazon.awscdk.services.iam.PolicyStatementProps;
import software.amazon.awscdk.services.iam.Role;
import software.amazon.awscdk.services.iam.RoleProps;
import software.amazon.awscdk.services.iam.ServicePrincipal;
import software.amazon.awscdk.services.lambda.Code;
import software.amazon.awscdk.services.lambda.Function;
import software.amazon.awscdk.services.lambda.Runtime;
import software.amazon.awscdk.services.stepfunctions.Chain;
import software.amazon.awscdk.services.stepfunctions.Choice;
import software.amazon.awscdk.services.stepfunctions.Condition;
import software.amazon.awscdk.services.stepfunctions.Fail;
import software.amazon.awscdk.services.stepfunctions.Pass;
import software.amazon.awscdk.services.stepfunctions.StateMachine;
import software.amazon.awscdk.services.stepfunctions.StateMachineType;
import software.amazon.awscdk.services.stepfunctions.tasks.LambdaInvoke;


public class TheStateMachineStack extends Stack {
    public TheStateMachineStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public TheStateMachineStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        // Step Function Starts Here

        // The first thing we need to do is see if they are asking for pineapple on a pizza
        Function pineappleCheckHandler = Function.Builder.create(this, "pineappleCheckLambdaHandler")
        		.runtime(Runtime.NODEJS_12_X) // execution environment
        		.code(Code.fromAsset("lambda_fns")) // code loaded from the "lambda_fns" directory
        		.handler("orderPizza.handler") // file is "orderPizza", function is "handler"
        		.build();
        
        /*
         * Step functions are built up of steps, we need to define our first step
         */
        LambdaInvoke orderPizzaTask = LambdaInvoke.Builder.create(this, "Order Pizza Job")
        		.lambdaFunction(pineappleCheckHandler)
        		.inputPath("$.flavour")
        		.resultPath("$.pineappleAnalysis")
        		.payloadResponseOnly(true)
        		.build();
        
        // Pizza Order failure step defined
        Fail jobFailed = Fail.Builder.create(this, "Sorry, We Dont add Pineapple")
        		.cause("They asked for Pineapple")
        		.error("Failed To Make Pizza")
        		.build();
        
        // If they didn't ask for pineapple let's cook the pizza
        Pass cookPizza = Pass.Builder.create(this, "Lets make your pizza")
        		.build();
        
        
        // If they ask for a pizza with pineapple, fail. Otherwise cook the pizza
        Chain chainDefinition = Chain
        		.start(orderPizzaTask)
        		.next(Choice.Builder.create(this, "With Pineapple?") // Logical choice added to flow
        				.build()
        				// Look at the "status" field
        				.when(Condition.booleanEquals("$.pineappleAnalysis.containsPineapple", true), jobFailed) // Fail for pineapple
        				.otherwise(cookPizza));
        
        // Building the state machine
        StateMachine stateMachine = StateMachine.Builder.create(this, "StateMachine")
        		.definition(chainDefinition)
        		.timeout(Duration.minutes(5))
        		.stateMachineType(StateMachineType.EXPRESS)
        		.build();
        
        /**
         * HTTP API Definition
         */
        
        // We need to give our HTTP API permission to invoke our step function
        Role httpApiRole = new Role(this, "HttpApiRole", new RoleProps.Builder()
        												.assumedBy(new ServicePrincipal("apigateway.amazonaws.com"))
        												.inlinePolicies(Map.of("AllowSFNExec", new PolicyDocument(
        														new PolicyDocumentProps.Builder()
        		        										.statements(List.of(new PolicyStatement(
        		        								        		new PolicyStatementProps.Builder()
        		        								        		.effect(Effect.ALLOW)
        		        								        		.resources(List.of(stateMachine.getStateMachineArn()))
        		        								        		.actions(List.of("states:StartSyncExecution"))
        		        								        		.build())))
        		        										.build())))
        												.build());
        
        HttpApi api = new HttpApi(this, "TheStateMachineAPI", new HttpApiProps.Builder().createDefaultStage(true).build());
        
        CfnIntegration integration = new CfnIntegration(this, "Integration", new CfnIntegrationProps.Builder()
        																	.apiId(api.getHttpApiId())
        																	.integrationType("AWS_PROXY")
        																	.connectionType("INTERNET")
        																	.integrationSubtype("StepFunctions-StartSyncExecution")
        																	.credentialsArn(httpApiRole.getRoleArn())
        																	.requestParameters(Map.of("Input","$request.body",
        																							  "StateMachineArn",stateMachine.getStateMachineArn()))
        																	.payloadFormatVersion("1.0")
        																	.timeoutInMillis(10000)
        																	.build());
        
        new CfnRoute(this, "DefaultRoute", new CfnRouteProps.Builder()
        		.apiId(api.getHttpApiId())
        		.routeKey(HttpRouteKey.DEFAULT.getKey())
        		.target("integrations/"+integration.getRef()).build());
        
        // output the URL of the HTTP API
        new CfnOutput(this, "HTTP API URL", new CfnOutputProps.Builder()
        		.value(api.getUrl()).build());
    }
}
