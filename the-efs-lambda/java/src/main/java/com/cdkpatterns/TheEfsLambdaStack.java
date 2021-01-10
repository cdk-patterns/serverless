package com.cdkpatterns;

import software.amazon.awscdk.core.*;
import software.amazon.awscdk.services.lambda.Code;
import software.amazon.awscdk.services.lambda.Function;
import software.amazon.awscdk.services.lambda.Runtime;
import software.amazon.awscdk.services.ec2.Vpc;
import software.amazon.awscdk.services.efs.FileSystem;
import software.amazon.awscdk.services.efs.AccessPoint;
import software.amazon.awscdk.services.efs.AccessPointOptions;
import software.amazon.awscdk.services.efs.Acl;
import software.amazon.awscdk.services.efs.PosixUser;
import software.amazon.awscdk.services.apigatewayv2.HttpApi;
import software.amazon.awscdk.services.apigatewayv2.integrations.LambdaProxyIntegration;

public class TheEfsLambdaStack extends Stack {
    public TheEfsLambdaStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public TheEfsLambdaStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        // EFS needs to be setup in a VPC
        Vpc vpc = Vpc.Builder.create(this, "Vpc")
        		.maxAzs(2)
        		.build();
        
        // Create a file system in EFS to store information
        FileSystem fileSystem = FileSystem.Builder.create(this, "FileSystem")
        		.vpc(vpc)
        		.removalPolicy(RemovalPolicy.DESTROY)
        		.build();
        
        // Create a access point to EFS
        AccessPoint accessPoint = fileSystem.addAccessPoint("AccessPoint", 
        		AccessPointOptions.builder()
        		.createAcl(
        				Acl
        				.builder()
        				.ownerGid("1001").ownerUid("1001").permissions("750")
        				.build())
        		.path("/export/lambda")
        		.posixUser(
        				PosixUser
        				.builder()
        				.gid("1001").uid("1001")
        				.build())
        		.build());
        
        // Create the lambda function
        Function efsLambda = Function.Builder.create(this, "efsLambdaFunction")
        		.runtime(Runtime.PYTHON_3_8)
        		.code(Code.fromAsset("lambda_fns"))
        		.handler("message_wall.lambda_handler")
        		.vpc(vpc)
        		.filesystem(software.amazon.awscdk.services.lambda.FileSystem.fromEfsAccessPoint(accessPoint, "/mnt/msg"))
        		.build();

        // Api Gateway HTTP integration
        HttpApi httpApi = HttpApi.Builder.create(this, "EFS Lambda")
        		.defaultIntegration(
        				LambdaProxyIntegration
        				.Builder
        				.create()
        				.handler(efsLambda)
        				.build())
        		.build();
        
        CfnOutput.Builder.create(this, "HTTP API Url")
        .value(httpApi.getUrl())
        .build();
    }
}
