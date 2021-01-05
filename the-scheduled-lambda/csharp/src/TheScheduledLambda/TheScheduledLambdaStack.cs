using Amazon.CDK;
using Lambda = Amazon.CDK.AWS.Lambda;
using Events = Amazon.CDK.AWS.Events;
using EventsTarget = Amazon.CDK.AWS.Events.Targets;
using DynamoDB = Amazon.CDK.AWS.DynamoDB;
using System.Collections.Generic;

namespace TheScheduledLambda
{
    public class TheScheduledLambdaStack : Stack
    {

        readonly private DynamoDB.Table _dynamoDbTable;
        readonly private Lambda.Function _functionScheduled;
        readonly private Events.Rule _ruleScheduled;


        internal TheScheduledLambdaStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {

            // DynamoDB Table
            _dynamoDbTable = new DynamoDB.Table(this, "RequestTable", new DynamoDB.TableProps
            {
                PartitionKey = new DynamoDB.Attribute
                {
                    Name = "requestid", Type = DynamoDB.AttributeType.STRING
                },
                RemovalPolicy = RemovalPolicy.DESTROY
            });

            // Create the Lambda function we want to run on a schedule
            _functionScheduled = new Lambda.Function(this, "ScheduledLambda", new Lambda.FunctionProps
            {
                Runtime = Lambda.Runtime.NODEJS_12_X, // execution environment
                Handler = "index.handler", // file is "index", function is "handler"
                Code = Lambda.Code.FromAsset("lambda_fns"), // code loaded from the "lambda_fns" directory,
                Environment = new Dictionary<string, string>
                {
                    { "TABLE_NAME", _dynamoDbTable.TableName }
                }
            });

            // Allow our lambda fn to write to the table
            _dynamoDbTable.GrantReadWriteData(_functionScheduled);

            // Create EventBridge rule that will execute our Lambda every 2 minutes
            _ruleScheduled = new Events.Rule(this, "scheduledLambda-schedule", new Events.RuleProps
            {
                Schedule = Events.Schedule.Expression("rate(2 minutes)")
            });

            // Set the target of our EventBridge rule to our Lambda function
            _ruleScheduled.AddTarget(new EventsTarget.LambdaFunction(_functionScheduled));

        }
    }
}
