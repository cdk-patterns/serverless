using Amazon.CDK;
using Lambda = Amazon.CDK.AWS.Lambda;
using DynamoDB = Amazon.CDK.AWS.DynamoDB;
using S3Assets = Amazon.CDK.AWS.S3.Assets;
using IAM = Amazon.CDK.AWS.IAM;
using AlexaAsk = Amazon.CDK.Alexa.Ask;
using System.Collections.Generic;

namespace TheAlexaSkill
{
    public class TheAlexaSkillStack : Stack
    {

        private readonly S3Assets.Asset _alexaAssets;
        private readonly IAM.Role _bucketRole;
        private readonly DynamoDB.Table _userTable;
        private readonly Lambda.Function _alexaFunction;
        private readonly AlexaAsk.CfnSkill _alexaSkill;

        internal TheAlexaSkillStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {

            // Assets for Alexa
            _alexaAssets = new S3Assets.Asset(this, "SkillAsset", new S3Assets.AssetProps
            {
                Path = "skill/"
            });

            // Role to access bucket
            _bucketRole = new IAM.Role(this, "Role", new IAM.RoleProps
            {
                AssumedBy = new IAM.CompositePrincipal(
                    new IAM.ServicePrincipal("alexa-appkit.amazon.com"),
                    new IAM.ServicePrincipal("cloudformation.amazonaws.com")
                )
            });

            // Allow the skill resource to access the zipped skill package
            _bucketRole.AddToPolicy(new IAM.PolicyStatement(
                new IAM.PolicyStatementProps
                    {
                        Actions = new[] { "S3:GetObject" },
                        Resources = new[] { "arn:aws:s3:::{" + _alexaAssets.S3BucketName + "}/{" + _alexaAssets.S3ObjectKey + "}" }
                    }
                )
            );

            // DynamoDB Table
            _userTable = new DynamoDB.Table(this, "Users", new DynamoDB.TableProps
            {
                PartitionKey = new DynamoDB.Attribute { 
                    Name = "userId",
                    Type = DynamoDB.AttributeType.STRING
                },
                BillingMode = DynamoDB.BillingMode.PAY_PER_REQUEST,
                RemovalPolicy = RemovalPolicy.DESTROY
            });

            // Lambda function for Alexa
            _alexaFunction = new Lambda.Function(this, "AlexaLambdaHandler", new Lambda.FunctionProps
            {
                Runtime = Lambda.Runtime.NODEJS_12_X,
                Code = Lambda.Code.FromAsset("lambda_fns"),
                Handler = "lambda.handler",
                Environment = new Dictionary<string, string>
                {
                    { "USERS_TABLE", _userTable.TableName }
                }
            });

            // grant the lambda role read / write permissions to our table
            _userTable.GrantReadWriteData(_alexaFunction);

            // create the skill
            _alexaSkill = new AlexaAsk.CfnSkill(this, "the-alexa-skill", new AlexaAsk.CfnSkillProps
            {
                VendorId = "",
                AuthenticationConfiguration = new AlexaAsk.CfnSkill.AuthenticationConfigurationProperty {
                    ClientId = "",
                    ClientSecret = "",
                    RefreshToken = ""
                },
                SkillPackage = new AlexaAsk.CfnSkill.SkillPackageProperty
                {
                    S3Bucket = _alexaAssets.S3BucketName,
                    S3Key = _alexaAssets.S3ObjectKey,
                    S3BucketRole = _bucketRole.RoleArn,
                    Overrides = new AlexaAsk.CfnSkill.OverridesProperty
                    {
                        Manifest = new Dictionary<string, object>
                        {
                            { "apis", new Dictionary<string, object>
                                {
                                    { "custom", new Dictionary<string, object>
                                        {
                                            { "endpoint", new Dictionary<string, object>
                                                {
                                                    { "uri", _alexaFunction.FunctionArn }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        } 
                    }
                } 
            });

            /*
             * Allow the Alexa service to invoke the fulfillment Lambda.
             * In order for the Skill to be created, the fulfillment Lambda
             * must have a permission allowing Alexa to invoke it, this causes
             * a circular dependency and requires the first deploy to allow all
             * Alexa skills to invoke the lambda, subsequent deploys will work
             * when specifying the eventSourceToken
             */
            _alexaFunction.AddPermission("AlexaPermission", new Lambda.Permission
            {
                EventSourceToken = _alexaSkill.Ref,
                Principal = new IAM.ServicePrincipal("alexa-appkit.amazon.com"),
                Action = "lambda:InvokeFunction"
            });
        }
    }
}
