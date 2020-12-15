using Amazon.CDK;
using Lambda = Amazon.CDK.AWS.Lambda;
using LambdaEvents = Amazon.CDK.AWS.Lambda.EventSources;
using APIG = Amazon.CDK.AWS.APIGateway;
using SQS = Amazon.CDK.AWS.SQS;
using DynamoDB = Amazon.CDK.AWS.DynamoDB;
using System.Collections.Generic;

namespace TheScalableWebhook
{
    public class TheScalableWebhookStack : Stack
    {
        // declaring all constructors
        readonly private DynamoDB.Table _dynamoDbTable;
        readonly private SQS.Queue _queue;
        readonly private Lambda.Function _functionPublish;
        readonly private Lambda.Function _functionSubscribe;

        internal TheScalableWebhookStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            /*
             * DynamoDB Table
             * This is standing in for what is RDS on the diagram due to simpler/cheaper setup
             */
            _dynamoDbTable = new DynamoDB.Table(this, "Messages", new DynamoDB.TableProps
            {
                PartitionKey = new DynamoDB.Attribute { Name = "id", Type = DynamoDB.AttributeType.STRING }
            });

            /*
             * Queue Setup
             */
            _queue = new SQS.Queue(this, "RDSPublishQueue", new SQS.QueueProps
            {
                VisibilityTimeout = Duration.Seconds(300)
            });

            /*
             * defines an AWS  Lambda resource to publish to our sqs_queue
             */
            _functionPublish = new Lambda.Function(this, "SQSPublishLambdaHandler", new Lambda.FunctionProps
            {
                Runtime = Lambda.Runtime.NODEJS_12_X,
                Handler = "lambda.handler",
                Code = Lambda.Code.FromAsset("lambda_fns/publish"),
                Environment = new Dictionary<string, string>
                {
                    { "queueURL", _queue.QueueUrl }
                }
            });

            _queue.GrantSendMessages(_functionPublish);

            /*
             * defines an AWS  Lambda resource to pull from our sqs_queue
             */
            _functionSubscribe = new Lambda.Function(this, "SQSSubscribeLambdaHandler", new Lambda.FunctionProps
            {
                Runtime = Lambda.Runtime.NODEJS_12_X,
                Handler = "lambda.handler",
                Code = Lambda.Code.FromAsset("lambda_fns/subscribe"),
                Environment = new Dictionary<string, string>
                {
                    { "queueURL", _queue.QueueUrl },
                    { "tableName", _dynamoDbTable.TableName }
                }
            });

            _queue.GrantConsumeMessages(_functionSubscribe);
            _functionSubscribe.AddEventSource(new LambdaEvents.SqsEventSource(_queue));
            _dynamoDbTable.GrantReadWriteData(_functionSubscribe);

            /*
             * defines an API Gateway REST API resource backed by our "sqs_publish_lambda" function.
             */
            new APIG.LambdaRestApi(this, "Endpoint", new APIG.LambdaRestApiProps
            {
                Handler = _functionPublish
            });

        }
    }
}
