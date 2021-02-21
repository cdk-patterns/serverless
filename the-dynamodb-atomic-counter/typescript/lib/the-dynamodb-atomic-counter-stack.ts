import * as cdk from '@aws-cdk/core';
import * as iam from '@aws-cdk/aws-iam';
import * as apigateway from '@aws-cdk/aws-apigateway';
import * as dynamodb from '@aws-cdk/aws-dynamodb';
import {AwsSdkCall, AwsCustomResource, AwsCustomResourcePolicy, PhysicalResourceId} from '@aws-cdk/custom-resources'

const configuration = {
  "tableName": "atomicCounter",
  "defaultResource": "counter"
}

export class TheDynamodbAtomicCounterStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /*
    * 1: Creating appropriate roles
    */
    // IAM Role for APIGateway
    let iamRole = new iam.Role(scope = this, id = "iam-role-apigw-stack-cdk", {
      roleName: "iam-role-apigw-stack-cdk",
      assumedBy: new iam.ServicePrincipal('apigateway.amazonaws.com'),
      managedPolicies: [iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonDynamoDBFullAccess')],
      path: "/service-role/"
    });
    // IAM Role for Lambda - Data insert
    let iamRoleLambda = new iam.Role(scope = this, id = "iam-role-lambda-stack-cdk", {
      roleName: "iam-role-lambda-stack-cdk",
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonDynamoDBFullAccess')],
      path: "/service-role/"
    });

    /*
    * 2: Creating the DynamoDB table with a Partition (PrimaryKey)
    */ 
    const dynamodbTable = new dynamodb.Table(scope = this, id = "dynamodb-table", {
      tableName: configuration["tableName"],
      partitionKey: {
        name: "atomicCounter",
        type: dynamodb.AttributeType.STRING
      },
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });

    /*
    * 3: We must insert initial data into DynamoDB table
    */
    const customPolicy = AwsCustomResourcePolicy.fromSdkCalls({ resources: AwsCustomResourcePolicy.ANY_RESOURCE });

    // Params for initial insert
    const createParams = {
      "TableName": configuration["tableName"],
      "Item": {
        "atomicCounter": {
          "S": "system-aa"
        },
        "counterValue": {
          "N": "1"
        }
      },
      "ConditionExpression": "attribute_not_exists(atomicCounter)"
    }

    // AwsSdkCall for putItem operation
    // https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.custom_resources/AwsSdkCall.html
    const dataResource = new AwsCustomResource(scope = this, id = "custom-populate-ddb", {
      logRetention: 0,
      policy: customPolicy,
      role: iamRoleLambda,
      onCreate: {
        service: "DynamoDB",
        action: "putItem",
        apiVersion: undefined,
        physicalResourceId: PhysicalResourceId.of('data-table'),
        parameters: createParams
      }
    });

    // The CFN must wait to finish the table creation before insert the data
    dataResource.node.addDependency(dynamodbTable);

    /*
    * 4: Creating Rest API Gateway
    */
    const apiGatewayAtomic = new apigateway.RestApi(scope = this, id = "atomic-counter-api", {
      restApiName: "Atomic Count API",
      description: "This API serve an Atomic Count API pattern.",
      endpointTypes: [apigateway.EndpointType.REGIONAL],
      deploy: true
    });

    /*
    * 5: Creating AWS Integration Service Response, Integration Options and Integration Service Method
    */
    const apiAwsIntegration = new apigateway.AwsIntegration({
      service: "dynamodb",
      action: "UpdateItem",
      integrationHttpMethod: "POST",
      options: {
        credentialsRole: iamRole,
        integrationResponses: [{
          statusCode: "200",
          responseTemplates: {
            "application/json": "#set($value = $input.json('Attributes.counterValue.N'))\r\n#set($l = $value.length())\r\n#set($l = $l - 1)\r\n$value.substring(1,$l)"
          }
        }],
        passthroughBehavior: apigateway.PassthroughBehavior.NEVER,
        requestTemplates: {
          "application/json": "{\r\n    \"TableName\": \""+configuration["tableName"]+"\",\r\n    \"Key\": {\r\n        \"atomicCounter\": {\r\n            \"S\": \"$input.params('systemKey')\"\r\n        }\r\n    },\r\n    \"UpdateExpression\": \"set counterValue = counterValue + :num\",\r\n    \"ExpressionAttributeValues\": {\r\n        \":num\": {\"N\": \"1\"}\r\n    },\r\n    \"ReturnValues\" : \"UPDATED_OLD\"\r\n}"
        }
      }
    });

    /*
    * 6: Adding resource /counter and method GET.
    */
    const methodApiGatewayAtomic = apiGatewayAtomic.root.addResource(configuration["defaultResource"]);
    methodApiGatewayAtomic.addMethod("GET", apiAwsIntegration, {
      methodResponses: [{
        statusCode: "200",
        responseModels: {
          "application/json": apigateway.Model.EMPTY_MODEL
        }
      }]
    });

    /*
    * 7: Output URL
    * The output url will be: https://xxx.execute-api.REGION.amazonaws.com/prod/counter
    */
    new cdk.CfnOutput(scope=this, id='apigw-counter-url', {
      value: `${apiGatewayAtomic.url}${configuration["defaultResource"]}?systemKey=system-aa`
    });
  }
}
