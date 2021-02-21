package com.cdkpatterns;

import java.util.List;
import java.util.Map;

import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.RemovalPolicy;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.core.StackProps;
import software.amazon.awscdk.services.s3.assets.Asset;
import software.amazon.awscdk.services.iam.Role;
import software.amazon.awscdk.services.iam.CompositePrincipal;
import software.amazon.awscdk.services.iam.ServicePrincipal;
import software.amazon.awscdk.services.iam.PolicyStatement;
import software.amazon.awscdk.services.iam.PolicyStatementProps;
import software.amazon.awscdk.services.dynamodb.Table;
import software.amazon.awscdk.services.dynamodb.Attribute;
import software.amazon.awscdk.services.dynamodb.AttributeType;
import software.amazon.awscdk.services.dynamodb.BillingMode;
import software.amazon.awscdk.services.lambda.Function;
import software.amazon.awscdk.services.lambda.Runtime;
import software.amazon.awscdk.services.lambda.Code;
import software.amazon.awscdk.services.lambda.Permission;
import software.amazon.awscdk.alexa.ask.CfnSkill;


public class TheAlexaSkillStack extends Stack {
    public TheAlexaSkillStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public TheAlexaSkillStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        // Assets for Alexa
        Asset alexaAssets = Asset.Builder.create(this, "SkillAsset")
        		.path("skill/")
        		.build();
        
        
        // Role to access bucket
        Role bucketRole = Role.Builder.create(this, "Role")
        		.assumedBy(new CompositePrincipal(
        				new ServicePrincipal("alexa-appkit.amazon.com"),
        				new ServicePrincipal("cloudformation.amazonaws.com")
        				))
        		.build();
        				
        // Allow the skill resource to access the zipped skill package
        bucketRole.addToPolicy(new PolicyStatement(
        		new PolicyStatementProps.Builder()
        			.actions(List.of("S3:GetObject"))
        			.resources(List.of("arn:aws:s3:::{" + alexaAssets.getS3BucketName() +  "}/{" + alexaAssets.getS3ObjectKey() + "}"))
        		.build()));
        
        // DynamoDB Table
        Table userTable = Table.Builder.create(this, "Users")
        		.partitionKey(new Attribute.Builder()
        				.name("userId")
        				.type(AttributeType.STRING)
        				.build())
        		.billingMode(BillingMode.PAY_PER_REQUEST)
        		.removalPolicy(RemovalPolicy.DESTROY)
        		.build();
        
        // Lambda function for Alexa
        Function alexaFunction = Function.Builder.create(this, "AlexaLambdaHandler")
        		.runtime(Runtime.NODEJS_12_X)
        		.code(Code.fromAsset("lambda_fns"))
        		.handler("lambda.handler")
        		.environment(Map.of(
        				"USERS_TABLE", userTable.getTableName()))
        		.build();
        
        // grant the lambda role read / write permissions to our table
        userTable.grantReadWriteData(alexaFunction);

        // create the skill
        CfnSkill alexaSkill = CfnSkill.Builder.create(this, "the-alexa-skill")
        		.vendorId("")
        		.authenticationConfiguration(
        				new CfnSkill.AuthenticationConfigurationProperty
        				.Builder()
        				.clientId("")
        				.clientSecret("")
        				.refreshToken("")
        				.build())
        		.skillPackage(
        				new CfnSkill.SkillPackageProperty
        				.Builder()
        				.s3Bucket(alexaAssets.getS3BucketName())
        				.s3Key(alexaAssets.getS3ObjectKey())
        				.s3BucketRole(bucketRole.getRoleArn())
        				.overrides(
        						new CfnSkill.OverridesProperty
        						.Builder()
        						.manifest(
        								Map.of("apis", 
        										Map.of("custom", 
        												Map.of("endpoint",
        														Map.of("uri", alexaFunction.getFunctionArn()
        																)
        														)
        												)
        										)
        								)
        						.build())
        				.build())
        		.build();
        		

        /*
         * Allow the Alexa service to invoke the fulfillment Lambda.
         * In order for the Skill to be created, the fulfillment Lambda
         * must have a permission allowing Alexa to invoke it, this causes
         * a circular dependency and requires the first deploy to allow all
         * Alexa skills to invoke the lambda, subsequent deploys will work
         * when specifying the eventSourceToken
         */
        alexaFunction.addPermission("AlexaPermission", 
        		new Permission.Builder()
        		.eventSourceToken(alexaSkill.getRef())
        		.principal(new ServicePrincipal("alexa-appkit.amazon.com"))
        		.action("lambda:InvokeFunction")
        		.build());
    }
}
