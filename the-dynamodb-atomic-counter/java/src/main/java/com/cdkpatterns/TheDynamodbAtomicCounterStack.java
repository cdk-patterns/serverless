package com.cdkpatterns;

import java.util.List;
import java.util.Map;

import software.amazon.awscdk.core.CfnOutput;
import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.RemovalPolicy;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.core.StackProps;
import software.amazon.awscdk.services.iam.Role;
import software.amazon.awscdk.services.iam.ServicePrincipal;
import software.amazon.awscdk.services.iam.ManagedPolicy;
import software.amazon.awscdk.services.dynamodb.Table;
import software.amazon.awscdk.services.dynamodb.Attribute;
import software.amazon.awscdk.services.dynamodb.AttributeType;
import software.amazon.awscdk.customresources.AwsCustomResource;
import software.amazon.awscdk.customresources.AwsCustomResourcePolicy;
import software.amazon.awscdk.customresources.AwsCustomResourceProps;
import software.amazon.awscdk.customresources.AwsSdkCall;
import software.amazon.awscdk.customresources.PhysicalResourceId;
import software.amazon.awscdk.customresources.SdkCallsPolicyOptions;
import software.amazon.awscdk.services.apigateway.RestApi;
import software.amazon.awscdk.services.apigateway.EndpointType;
import software.amazon.awscdk.services.apigateway.IntegrationOptions;
import software.amazon.awscdk.services.apigateway.IntegrationResponse;
import software.amazon.awscdk.services.apigateway.MethodOptions;
import software.amazon.awscdk.services.apigateway.MethodResponse;
import software.amazon.awscdk.services.apigateway.Model;
import software.amazon.awscdk.services.apigateway.PassthroughBehavior;
import software.amazon.awscdk.services.apigateway.Resource;
import software.amazon.awscdk.services.apigateway.AwsIntegration;


public class TheDynamodbAtomicCounterStack extends Stack {
	
	private String tableName = "atomicCounter";
    private String defaultResource = "counter";
	
    public TheDynamodbAtomicCounterStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public TheDynamodbAtomicCounterStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        /*
         * 1: Creating appropriate roles
         */

        // IAM Role for APIGateway
        Role iamRoleForApiGateway = Role.Builder.create(this, "iam-role-apigw-stack-cdk")
        		.roleName("iam-role-apigw-stack-cdk")
        		.assumedBy(new ServicePrincipal("apigateway.amazonaws.com"))
        		.managedPolicies(List.of(
        				ManagedPolicy.fromAwsManagedPolicyName("AmazonDynamoDBFullAccess")
        				))
        		.path("/service-role/")
        		.build();

        // IAM Role for Lambda - Data insert
        Role iamRoleForLambda = Role.Builder.create(this, "iam-role-lambda-stack-cdk")
        		.roleName("iam-role-lambda-stack-cdk")
        		.assumedBy(new ServicePrincipal("lambda.amazonaws.com"))
        		.managedPolicies(List.of(
        				ManagedPolicy.fromAwsManagedPolicyName("AmazonDynamoDBFullAccess")
        				))
        		.path("/service-role/")
        		.build();
        
        /*
         * 2: Creating the DynamoDB table with a Partition(PrimaryKey)
         */
        Attribute partitionKey = new Attribute
        		.Builder()
        		.name("atomicCounter")
        		.type(AttributeType.STRING)
        		.build();

        Table tableAtomicCounter = Table.Builder.create(this, "dynamodb-table")
        		.tableName(tableName)
        		.partitionKey(partitionKey)
        		.removalPolicy(RemovalPolicy.DESTROY)
        		.build();
        
        /*
         * 3: We must insert initial data into DynamoDB table
         */
        AwsCustomResourcePolicy customPolicy = AwsCustomResourcePolicy.fromSdkCalls(
        		new SdkCallsPolicyOptions.Builder().resources(AwsCustomResourcePolicy.ANY_RESOURCE)
        		.build()
        		);
        
        // Params for initial insert
        Map<String, Object> createParams = Map.ofEntries(
        		Map.entry("TableName", tableName),
                Map.entry("Item", Map.ofEntries(
                        Map.entry("atomicCounter", Map.of("S", "system-aa")),
                        Map.entry("counterValue", Map.of("N", "1"))
                )),
                Map.entry("ConditionExpression", "attribute_not_exists(atomicCounter)"));
        
        // AwsSdkCall for putItem operation
        // https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.custom_resources/AwsSdkCall.html
        AwsSdkCall dataTable = new AwsSdkCall.Builder()
        		.service("DynamoDB")
        		.action("putItem")
        		.physicalResourceId(PhysicalResourceId.of("data-table"))
        		.parameters(createParams)
        		.build();
        
        // AwsCustomResource for putItem operation
        // https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.custom_resources/AwsCustomResource.html
        AwsCustomResource dataResource = new AwsCustomResource(this, "custom-populate-ddb",
        		new AwsCustomResourceProps.Builder()
        		.policy(customPolicy)
        		.logRetention(null)
        		.role(iamRoleForLambda)
        		.onCreate(dataTable)
        		.onUpdate(dataTable)
        		.build());
        
        // The CFN must wait to finish the table creation before insert the data
        dataResource.getNode().addDependency(tableAtomicCounter);

        /*
         * 4: Creating Rest API Gateway
         */
        RestApi apiGatewayAtomic = RestApi.Builder.create(this, "atomic-counter-api")
        		.restApiName("Atomic Count API")
        		.description("This API serve an Atomic Count API pattern.")
        		.endpointTypes(List.of(EndpointType.REGIONAL))
        		.deploy(true)
        		.build();
        
        
        String responseTemplate = "#set($value = $input.json('Attributes.counterValue.N'))\r\n#set($l = $value.length())\r\n#set($l = $l - 1)\r\n$value.substring(1,$l)";
        String requestTemplate = "{\r\n    \"TableName\": \""+tableName+ "\",\r\n    \"Key\": {\r\n        \"atomicCounter\": {\r\n            \"S\": \"$input.params('systemKey')\"\r\n        }\r\n    },\r\n    \"UpdateExpression\": \"set counterValue = counterValue + :num\",\r\n    \"ExpressionAttributeValues\": {\r\n        \":num\": {\"N\": \"1\"}\r\n    },\r\n    \"ReturnValues\" : \"UPDATED_OLD\"\r\n}";
        
        AwsIntegration awsIntegragion = AwsIntegration
        		.Builder
        		.create()
        		.service("dynamodb")
        		.action("UpdateItem")
        		.integrationHttpMethod("POST")
        		.options(new IntegrationOptions.Builder()
        				.credentialsRole(iamRoleForApiGateway)
        				.integrationResponses(List.of(
        						new IntegrationResponse
        						.Builder()
        						.statusCode("200")
        						.responseTemplates(Map.of(
        								"application/json", responseTemplate))
        						.build()
        						))
        				.passthroughBehavior(PassthroughBehavior.NEVER)
        				.requestTemplates(Map.of(
        						"application/json", requestTemplate))
        				.build())
        		.build();
        
        		
        /*
         * 6: Adding resource /counter and method GET.
         */
        Resource methodApiGatewayAtomic = apiGatewayAtomic.getRoot().addResource(defaultResource);
        methodApiGatewayAtomic.addMethod("GET", awsIntegragion, new MethodOptions
        		.Builder()
        		.methodResponses(List.of(
        				new MethodResponse
        				.Builder()
        				.statusCode("200")
        				.responseModels(Map.of(
        						"application/json", Model.EMPTY_MODEL
        						))
        				.build()))
        		.build());
        
        /*
         * 7: Output URL
         * The output url will be: https://xxx.execute-api.REGION.amazonaws.com/prod/counter
         */
        CfnOutput.Builder.create(this, "apigw-counter-url")
        	.value(apiGatewayAtomic.getUrl() + defaultResource + "?systemKey=system-aa")
        	.build();
    }
}
