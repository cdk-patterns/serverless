using Amazon.CDK;
using dynamoDB = Amazon.CDK.AWS.DynamoDB;
using apiGateway = Amazon.CDK.AWS.APIGateway;
using iam = Amazon.CDK.AWS.IAM;
using awsSdkCall = Amazon.CDK.CustomResources.AwsSdkCall;
using awsCustomResource = Amazon.CDK.CustomResources.AwsCustomResource;
using awsCustomResourcePolicy = Amazon.CDK.CustomResources.AwsCustomResourcePolicy;
using physicalResourceId = Amazon.CDK.CustomResources.PhysicalResourceId;
using System.Collections.Generic;
using Amazon.CDK.CustomResources;

namespace TheDynamodbAtomicCounter
{

    public class TheDynamodbAtomicCounterStack : Stack
    {
        readonly private string _tableName = "atomicCounter";
        readonly private string _defaultResource = "counter";
        readonly private iam.Role _iamRoleForApiGateway;
        readonly private iam.Role _iamRoleForLambda;
        readonly private dynamoDB.Attribute _partitionKey;
        readonly private dynamoDB.Table _tableAtomicCounter;
        readonly private apiGateway.RestApi _apiGatewayAtomic;
        readonly private apiGateway.AwsIntegration _awsIntegragion;


        internal TheDynamodbAtomicCounterStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            /*
             * 1: Creating appropriate roles
             */

            // IAM Role for APIGateway
            _iamRoleForApiGateway = new iam.Role(this, "iam-role-apigw-stack-cdk", new iam.RoleProps
            {
                RoleName = "iam-role-apigw-stack-cdk",
                AssumedBy = new iam.ServicePrincipal("apigateway.amazonaws.com"),
                ManagedPolicies = new[] { iam.ManagedPolicy.FromAwsManagedPolicyName("AmazonDynamoDBFullAccess") },
                Path = "/service-role/"
            });

            // IAM Role for Lambda - Data insert
            _iamRoleForLambda = new iam.Role(this, "iam-role-lambda-stack-cdk", new iam.RoleProps
            {
                RoleName = "iam-role-lambda-stack-cdk",
                AssumedBy = new iam.ServicePrincipal("lambda.amazonaws.com"),
                ManagedPolicies = new[] { iam.ManagedPolicy.FromAwsManagedPolicyName("AmazonDynamoDBFullAccess") },
                Path = "/service-role/"
            });

            /*
             * 2: Creating the DynamoDB table with a Partition(PrimaryKey)
             */
            _partitionKey = new dynamoDB.Attribute
            {
                Name = "atomicCounter",
                Type = dynamoDB.AttributeType.STRING
            };

            _tableAtomicCounter = new dynamoDB.Table(this, "dynamodb-table", new dynamoDB.TableProps
            {
                TableName = _tableName,
                PartitionKey = _partitionKey,
                RemovalPolicy = RemovalPolicy.DESTROY
            });

            /*
             * 3: We must insert initial data into DynamoDB table
             */

            var customPolicy = awsCustomResourcePolicy.FromSdkCalls( new SdkCallsPolicyOptions
            {
                Resources = awsCustomResourcePolicy.ANY_RESOURCE
            });

            // Params for initial insert
            Dictionary<string, object> createParams = new Dictionary<string, object>
            {
                { "TableName", _tableName},
                { "Item", new Dictionary<string, object>
                    {
                        { "atomicCounter", new Dictionary<string, string>
                            {
                                { "S", "system-aa" }
                            }
                        },
                        { "counterValue", new Dictionary<string, string>
                            {
                                { "N", "1" }
                            }
                        },
                    }
                },
                { "ConditionExpression",  "attribute_not_exists(atomicCounter)" }
            };

            // AwsSdkCall for putItem operation
            // https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.custom_resources/AwsSdkCall.html
            var dataTable = new awsSdkCall
            {
                Service = "DynamoDB",
                Action = "putItem",
                PhysicalResourceId = physicalResourceId.Of("data-table"),
                Parameters = createParams
            };

            // AwsCustomResource for putItem operation
            // https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.custom_resources/AwsCustomResource.html
            var dataResource = new awsCustomResource(this, "custom-populate-ddb", new AwsCustomResourceProps
            {
                Policy = customPolicy,
                LogRetention = 0,
                Role = _iamRoleForLambda,
                OnCreate = dataTable,
                OnUpdate = dataTable
            });

            // The CFN must wait to finish the table creation before insert the data
            dataResource.Node.AddDependency(_tableAtomicCounter);

            /*
             * 4: Creating Rest API Gateway
             */

            _apiGatewayAtomic = new apiGateway.RestApi(this, "atomic-counter-api", new apiGateway.RestApiProps
            {
                RestApiName = "Atomic Count API",
                Description = "This API serve an Atomic Count API pattern.",
                EndpointTypes = new[] { apiGateway.EndpointType.REGIONAL },
                Deploy = true
            });

            /*
            * 5: Creating AWS Integration Service Response, Integration Options and Integration Service Method
            */

            Dictionary<string, string> responseTemplate = new Dictionary<string, string>();
            responseTemplate.Add("application/json", "#set($value = $input.json('Attributes.counterValue.N'))\r\n#set($l = $value.length())\r\n#set($l = $l - 1)\r\n$value.substring(1,$l)");

            Dictionary<string, string> requestTemplate = new Dictionary<string, string>();
            requestTemplate.Add("application/json", "{\r\n    \"TableName\": \""+_tableName+ "\",\r\n    \"Key\": {\r\n        \"atomicCounter\": {\r\n            \"S\": \"$input.params('systemKey')\"\r\n        }\r\n    },\r\n    \"UpdateExpression\": \"set counterValue = counterValue + :num\",\r\n    \"ExpressionAttributeValues\": {\r\n        \":num\": {\"N\": \"1\"}\r\n    },\r\n    \"ReturnValues\" : \"UPDATED_OLD\"\r\n}");
            
            _awsIntegragion = new apiGateway.AwsIntegration(new apiGateway.AwsIntegrationProps
            {
                Service = "dynamodb",
                Action = "UpdateItem",
                IntegrationHttpMethod = "POST",
                Options = new apiGateway.IntegrationOptions
                {
                    CredentialsRole = _iamRoleForApiGateway,
                    IntegrationResponses = new[] { new apiGateway.IntegrationResponse
                        {
                            StatusCode = "200",
                            ResponseTemplates = responseTemplate
                        }
                    },
                    PassthroughBehavior = apiGateway.PassthroughBehavior.NEVER,
                    RequestTemplates = requestTemplate
                }
            });

            /*
            * 6: Adding resource /counter and method GET.
            */
            Dictionary<string, apiGateway.IModel> responseModel = new Dictionary<string, apiGateway.IModel>();
            responseModel.Add("application/json", apiGateway.Model.EMPTY_MODEL);

            var methodApiGatewayAtomic = _apiGatewayAtomic.Root.AddResource(_defaultResource);
            methodApiGatewayAtomic.AddMethod("GET", _awsIntegragion, new apiGateway.MethodOptions
            {
                MethodResponses = new[] { new apiGateway.MethodResponse
                    {
                        StatusCode = "200",
                        ResponseModels = responseModel
                    }
                }
            });

            /*
            * 7: Output URL
            * The output url will be: https://xxx.execute-api.REGION.amazonaws.com/prod/counter
            */
            new CfnOutput(this, "apigw-counter-url", new CfnOutputProps
            {
                Value = _apiGatewayAtomic.Url + _defaultResource + "?systemKey=system-aa"
            });
        }
    }
}
