using Amazon.CDK;
using Lambda = Amazon.CDK.AWS.Lambda;
using APIGv2 = Amazon.CDK.AWS.APIGatewayv2;
using EC2 = Amazon.CDK.AWS.EC2;
using EFS = Amazon.CDK.AWS.EFS;
using APIGv2Integration = Amazon.CDK.AWS.APIGatewayv2.Integrations;

namespace TheEfsLambda
{
    public class TheEfsLambdaStack : Stack
    {
        // declaring all constructors
        readonly private EC2.Vpc _vpc;
        readonly private EFS.FileSystem _fileSystem;
        readonly private Lambda.Function _functionProxyHandler;
        readonly private APIGv2.HttpApi _apiGateway;

        internal TheEfsLambdaStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            // EFS needs to be setup in a VPC with 2Azs
            _vpc = new EC2.Vpc(this, "Vpc", new EC2.VpcProps
            {
                MaxAzs = 2
            });

            // Create a file system in EFS to store information
            _fileSystem = new EFS.FileSystem(this, "Filesystem", new EFS.FileSystemProps
            {
                Vpc = _vpc,
                RemovalPolicy = RemovalPolicy.DESTROY
            });

            // Create a access point to EFS
            EFS.AccessPoint accessPoint;
            accessPoint = _fileSystem.AddAccessPoint("AccessPoint", new EFS.AccessPointOptions
            {
                CreateAcl = new EFS.Acl { OwnerGid = "1001", OwnerUid = "1001", Permissions = "750"},
                Path = "/export/lambda",
                PosixUser = new EFS.PosixUser { Gid = "1001", Uid = "1001", }
            });

            // Create the lambda function
            _functionProxyHandler = new Lambda.Function(this, "efsLambdaFunction", new Lambda.FunctionProps
            {
                Runtime = Lambda.Runtime.PYTHON_3_8,
                Code = Lambda.Code.FromAsset("lambda_fns"),
                Handler = "message_wall.lambda_handler",
                Vpc = _vpc,
                Filesystem = Lambda.FileSystem.FromEfsAccessPoint(accessPoint, "/mnt/msg")
            });

            // Api Gateway HTTP integration
            _apiGateway = new APIGv2.HttpApi(this, "EFS Lambda", new APIGv2.HttpApiProps
            {
                DefaultIntegration = new APIGv2Integration.LambdaProxyIntegration(new APIGv2Integration.LambdaProxyIntegrationProps
                {
                    Handler = _functionProxyHandler
                })
            });


            // Output to CFN
            new CfnOutput(this, "HTTP API Url", new CfnOutputProps
            {
                Value = _apiGateway.Url
            });
        }
    }
}
