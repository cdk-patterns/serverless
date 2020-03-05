"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const cdk = require("@aws-cdk/core");
const lambda = require("@aws-cdk/aws-lambda");
const apigw = require("@aws-cdk/aws-apigateway");
const dynamodb = require("@aws-cdk/aws-dynamodb");
class TheSimpleGraphqlServiceStack extends cdk.Stack {
    constructor(scope, id, props) {
        super(scope, id, props);
        //DynamoDB Table
        const table = new dynamodb.Table(this, 'Hits', {
            partitionKey: { name: 'path', type: dynamodb.AttributeType.STRING }
        });
        // defines an AWS Lambda resource
        const dynamoLambda = new lambda.Function(this, 'DynamoLambdaHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,
            code: lambda.Code.asset('lambda'),
            handler: 'lambda.handler',
            environment: {
                HITS_TABLE_NAME: table.tableName
            }
        });
        // grant the lambda role read/write permissions to our table
        table.grantReadWriteData(dynamoLambda);
        // defines an API Gateway REST API resource backed by our "dynamoLambda" function.
        new apigw.LambdaRestApi(this, 'Endpoint', {
            handler: dynamoLambda
        });
    }
}
exports.TheSimpleGraphqlServiceStack = TheSimpleGraphqlServiceStack;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidGhlLXNpbXBsZS13ZWJzZXJ2aWNlLXN0YWNrLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsidGhlLXNpbXBsZS13ZWJzZXJ2aWNlLXN0YWNrLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7O0FBQUEscUNBQXFDO0FBQ3JDLDhDQUErQztBQUMvQyxpREFBa0Q7QUFDbEQsa0RBQW1EO0FBRW5ELE1BQWEsd0JBQXlCLFNBQVEsR0FBRyxDQUFDLEtBQUs7SUFDckQsWUFBWSxLQUFvQixFQUFFLEVBQVUsRUFBRSxLQUFzQjtRQUNsRSxLQUFLLENBQUMsS0FBSyxFQUFFLEVBQUUsRUFBRSxLQUFLLENBQUMsQ0FBQztRQUV4QixnQkFBZ0I7UUFDaEIsTUFBTSxLQUFLLEdBQUcsSUFBSSxRQUFRLENBQUMsS0FBSyxDQUFDLElBQUksRUFBRSxNQUFNLEVBQUU7WUFDN0MsWUFBWSxFQUFFLEVBQUUsSUFBSSxFQUFFLE1BQU0sRUFBRSxJQUFJLEVBQUUsUUFBUSxDQUFDLGFBQWEsQ0FBQyxNQUFNLEVBQUU7U0FDcEUsQ0FBQyxDQUFDO1FBRUYsaUNBQWlDO1FBQ2pDLE1BQU0sWUFBWSxHQUFHLElBQUksTUFBTSxDQUFDLFFBQVEsQ0FBQyxJQUFJLEVBQUUscUJBQXFCLEVBQUU7WUFDckUsT0FBTyxFQUFFLE1BQU0sQ0FBQyxPQUFPLENBQUMsV0FBVztZQUNuQyxJQUFJLEVBQUUsTUFBTSxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsUUFBUSxDQUFDO1lBQ2pDLE9BQU8sRUFBRSxnQkFBZ0I7WUFDekIsV0FBVyxFQUFFO2dCQUNYLGVBQWUsRUFBRSxLQUFLLENBQUMsU0FBUzthQUNuQztTQUNBLENBQUMsQ0FBQztRQUVGLDREQUE0RDtRQUM1RCxLQUFLLENBQUMsa0JBQWtCLENBQUMsWUFBWSxDQUFDLENBQUM7UUFFeEMsa0ZBQWtGO1FBQ2xGLElBQUksS0FBSyxDQUFDLGFBQWEsQ0FBQyxJQUFJLEVBQUUsVUFBVSxFQUFFO1lBQ3hDLE9BQU8sRUFBRSxZQUFZO1NBQ3RCLENBQUMsQ0FBQztJQUNMLENBQUM7Q0FDRjtBQTNCRCw0REEyQkMiLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBjZGsgZnJvbSAnQGF3cy1jZGsvY29yZSc7XG5pbXBvcnQgbGFtYmRhID0gcmVxdWlyZSgnQGF3cy1jZGsvYXdzLWxhbWJkYScpO1xuaW1wb3J0IGFwaWd3ID0gcmVxdWlyZSgnQGF3cy1jZGsvYXdzLWFwaWdhdGV3YXknKTtcbmltcG9ydCBkeW5hbW9kYiA9IHJlcXVpcmUoJ0Bhd3MtY2RrL2F3cy1keW5hbW9kYicpO1xuXG5leHBvcnQgY2xhc3MgVGhlU2ltcGxlV2Vic2VydmljZVN0YWNrIGV4dGVuZHMgY2RrLlN0YWNrIHtcbiAgY29uc3RydWN0b3Ioc2NvcGU6IGNkay5Db25zdHJ1Y3QsIGlkOiBzdHJpbmcsIHByb3BzPzogY2RrLlN0YWNrUHJvcHMpIHtcbiAgICBzdXBlcihzY29wZSwgaWQsIHByb3BzKTtcblxuICAgIC8vRHluYW1vREIgVGFibGVcbiAgICBjb25zdCB0YWJsZSA9IG5ldyBkeW5hbW9kYi5UYWJsZSh0aGlzLCAnSGl0cycsIHtcbiAgICAgIHBhcnRpdGlvbktleTogeyBuYW1lOiAncGF0aCcsIHR5cGU6IGR5bmFtb2RiLkF0dHJpYnV0ZVR5cGUuU1RSSU5HIH1cbiAgICB9KTtcblxuICAgICAvLyBkZWZpbmVzIGFuIEFXUyBMYW1iZGEgcmVzb3VyY2VcbiAgICAgY29uc3QgZHluYW1vTGFtYmRhID0gbmV3IGxhbWJkYS5GdW5jdGlvbih0aGlzLCAnRHluYW1vTGFtYmRhSGFuZGxlcicsIHtcbiAgICAgIHJ1bnRpbWU6IGxhbWJkYS5SdW50aW1lLk5PREVKU18xMl9YLCAgICAgIC8vIGV4ZWN1dGlvbiBlbnZpcm9ubWVudFxuICAgICAgY29kZTogbGFtYmRhLkNvZGUuYXNzZXQoJ2xhbWJkYScpLCAgLy8gY29kZSBsb2FkZWQgZnJvbSB0aGUgXCJsYW1iZGFcIiBkaXJlY3RvcnlcbiAgICAgIGhhbmRsZXI6ICdsYW1iZGEuaGFuZGxlcicsICAgICAgICAgICAgICAgIC8vIGZpbGUgaXMgXCJsYW1iZGFcIiwgZnVuY3Rpb24gaXMgXCJoYW5kbGVyXCJcbiAgICAgIGVudmlyb25tZW50OiB7XG4gICAgICAgIEhJVFNfVEFCTEVfTkFNRTogdGFibGUudGFibGVOYW1lXG4gICAgfVxuICAgIH0pO1xuXG4gICAgIC8vIGdyYW50IHRoZSBsYW1iZGEgcm9sZSByZWFkL3dyaXRlIHBlcm1pc3Npb25zIHRvIG91ciB0YWJsZVxuICAgICB0YWJsZS5ncmFudFJlYWRXcml0ZURhdGEoZHluYW1vTGFtYmRhKTtcblxuICAgIC8vIGRlZmluZXMgYW4gQVBJIEdhdGV3YXkgUkVTVCBBUEkgcmVzb3VyY2UgYmFja2VkIGJ5IG91ciBcImR5bmFtb0xhbWJkYVwiIGZ1bmN0aW9uLlxuICAgIG5ldyBhcGlndy5MYW1iZGFSZXN0QXBpKHRoaXMsICdFbmRwb2ludCcsIHtcbiAgICAgIGhhbmRsZXI6IGR5bmFtb0xhbWJkYVxuICAgIH0pO1xuICB9XG59XG4iXX0=