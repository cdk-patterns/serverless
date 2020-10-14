"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const cdk = require("@aws-cdk/core");
const lambda = require("@aws-cdk/aws-lambda");
const dynamodb = require("@aws-cdk/aws-dynamodb");
const apigw = require("@aws-cdk/aws-apigatewayv2");
const { execSync } = require('child_process');
class TheLambdaCircuitBreakerStack extends cdk.Stack {
    constructor(scope, id, props) {
        var _a;
        super(scope, id, props);
        //DynamoDB Table To Hold Circuitbreaker State
        const table = new dynamodb.Table(this, 'CircuitBreakerTable', {
            partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
            removalPolicy: cdk.RemovalPolicy.DESTROY
        });
        // Compile Lambda Function
        execSync('cd lambda-fns && npm i && npm run build');
        // Create a Lambda Function with unreliable code
        const unreliableLambda = new lambda.Function(this, 'DynamoLambdaHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,
            code: lambda.Code.fromAsset('lambda-fns'),
            handler: 'lambda.handler',
            environment: {
                CIRCUITBREAKER_TABLE: table.tableName
            }
        });
        // grant the lambda role read/write permissions to our table
        table.grantReadWriteData(unreliableLambda);
        // defines an API Gateway Http API resource backed by our "dynamoLambda" function.
        let api = new apigw.HttpApi(this, 'CircuitBreakerGateway', {
            defaultIntegration: new apigw.LambdaProxyIntegration({
                handler: unreliableLambda
            })
        });
        new cdk.CfnOutput(this, 'HTTP API Url', {
            value: (_a = api.url, (_a !== null && _a !== void 0 ? _a : 'Something went wrong with the deploy'))
        });
    }
}
exports.TheLambdaCircuitBreakerStack = TheLambdaCircuitBreakerStack;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidGhlLWxhbWJkYS1jaXJjdWl0LWJyZWFrZXItc3RhY2suanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyJ0aGUtbGFtYmRhLWNpcmN1aXQtYnJlYWtlci1zdGFjay50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOztBQUFBLHFDQUFxQztBQUNyQyw4Q0FBK0M7QUFDL0Msa0RBQW1EO0FBQ25ELG1EQUFvRDtBQUNwRCxNQUFNLEVBQUUsUUFBUSxFQUFFLEdBQUcsT0FBTyxDQUFDLGVBQWUsQ0FBQyxDQUFDO0FBRTlDLE1BQWEsNEJBQTZCLFNBQVEsR0FBRyxDQUFDLEtBQUs7SUFDekQsWUFBWSxLQUFvQixFQUFFLEVBQVUsRUFBRSxLQUFzQjs7UUFDbEUsS0FBSyxDQUFDLEtBQUssRUFBRSxFQUFFLEVBQUUsS0FBSyxDQUFDLENBQUM7UUFFeEIsNkNBQTZDO1FBQzdDLE1BQU0sS0FBSyxHQUFHLElBQUksUUFBUSxDQUFDLEtBQUssQ0FBQyxJQUFJLEVBQUUscUJBQXFCLEVBQUU7WUFDNUQsWUFBWSxFQUFFLEVBQUUsSUFBSSxFQUFFLElBQUksRUFBRSxJQUFJLEVBQUUsUUFBUSxDQUFDLGFBQWEsQ0FBQyxNQUFNLEVBQUU7WUFDakUsYUFBYSxFQUFFLEdBQUcsQ0FBQyxhQUFhLENBQUMsT0FBTztTQUN6QyxDQUFDLENBQUM7UUFFSCwwQkFBMEI7UUFDMUIsUUFBUSxDQUFDLHlDQUF5QyxDQUFDLENBQUM7UUFFcEQsZ0RBQWdEO1FBQ2hELE1BQU0sZ0JBQWdCLEdBQUcsSUFBSSxNQUFNLENBQUMsUUFBUSxDQUFDLElBQUksRUFBRSxxQkFBcUIsRUFBRTtZQUN4RSxPQUFPLEVBQUUsTUFBTSxDQUFDLE9BQU8sQ0FBQyxXQUFXO1lBQ25DLElBQUksRUFBRSxNQUFNLENBQUMsSUFBSSxDQUFDLFNBQVMsQ0FBQyxZQUFZLENBQUM7WUFDekMsT0FBTyxFQUFFLGdCQUFnQjtZQUN6QixXQUFXLEVBQUU7Z0JBQ1gsb0JBQW9CLEVBQUUsS0FBSyxDQUFDLFNBQVM7YUFDdEM7U0FDRixDQUFDLENBQUM7UUFFSCw0REFBNEQ7UUFDNUQsS0FBSyxDQUFDLGtCQUFrQixDQUFDLGdCQUFnQixDQUFDLENBQUM7UUFFM0Msa0ZBQWtGO1FBQ2xGLElBQUksR0FBRyxHQUFHLElBQUksS0FBSyxDQUFDLE9BQU8sQ0FBQyxJQUFJLEVBQUUsdUJBQXVCLEVBQUU7WUFDekQsa0JBQWtCLEVBQUUsSUFBSSxLQUFLLENBQUMsc0JBQXNCLENBQUM7Z0JBQ25ELE9BQU8sRUFBRSxnQkFBZ0I7YUFDMUIsQ0FBQztTQUNILENBQUMsQ0FBQztRQUVKLElBQUksR0FBRyxDQUFDLFNBQVMsQ0FBQyxJQUFJLEVBQUUsY0FBYyxFQUFFO1lBQ3RDLEtBQUssUUFBRSxHQUFHLENBQUMsR0FBRyx1Q0FBSSxzQ0FBc0MsRUFBQTtTQUN6RCxDQUFDLENBQUM7SUFDSixDQUFDO0NBQ0Y7QUFyQ0Qsb0VBcUNDIiwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgY2RrIGZyb20gJ0Bhd3MtY2RrL2NvcmUnO1xuaW1wb3J0IGxhbWJkYSA9IHJlcXVpcmUoJ0Bhd3MtY2RrL2F3cy1sYW1iZGEnKTtcbmltcG9ydCBkeW5hbW9kYiA9IHJlcXVpcmUoJ0Bhd3MtY2RrL2F3cy1keW5hbW9kYicpO1xuaW1wb3J0IGFwaWd3ID0gcmVxdWlyZSgnQGF3cy1jZGsvYXdzLWFwaWdhdGV3YXl2MicpO1xuY29uc3QgeyBleGVjU3luYyB9ID0gcmVxdWlyZSgnY2hpbGRfcHJvY2VzcycpO1xuXG5leHBvcnQgY2xhc3MgVGhlTGFtYmRhQ2lyY3VpdEJyZWFrZXJTdGFjayBleHRlbmRzIGNkay5TdGFjayB7XG4gIGNvbnN0cnVjdG9yKHNjb3BlOiBjZGsuQ29uc3RydWN0LCBpZDogc3RyaW5nLCBwcm9wcz86IGNkay5TdGFja1Byb3BzKSB7XG4gICAgc3VwZXIoc2NvcGUsIGlkLCBwcm9wcyk7XG5cbiAgICAvL0R5bmFtb0RCIFRhYmxlIFRvIEhvbGQgQ2lyY3VpdGJyZWFrZXIgU3RhdGVcbiAgICBjb25zdCB0YWJsZSA9IG5ldyBkeW5hbW9kYi5UYWJsZSh0aGlzLCAnQ2lyY3VpdEJyZWFrZXJUYWJsZScsIHtcbiAgICAgIHBhcnRpdGlvbktleTogeyBuYW1lOiAnaWQnLCB0eXBlOiBkeW5hbW9kYi5BdHRyaWJ1dGVUeXBlLlNUUklORyB9LFxuICAgICAgcmVtb3ZhbFBvbGljeTogY2RrLlJlbW92YWxQb2xpY3kuREVTVFJPWVxuICAgIH0pO1xuICAgIFxuICAgIC8vIENvbXBpbGUgTGFtYmRhIEZ1bmN0aW9uXG4gICAgZXhlY1N5bmMoJ2NkIGxhbWJkYS1mbnMgJiYgbnBtIGkgJiYgbnBtIHJ1biBidWlsZCcpO1xuXG4gICAgLy8gQ3JlYXRlIGEgTGFtYmRhIEZ1bmN0aW9uIHdpdGggdW5yZWxpYWJsZSBjb2RlXG4gICAgY29uc3QgdW5yZWxpYWJsZUxhbWJkYSA9IG5ldyBsYW1iZGEuRnVuY3Rpb24odGhpcywgJ0R5bmFtb0xhbWJkYUhhbmRsZXInLCB7XG4gICAgICBydW50aW1lOiBsYW1iZGEuUnVudGltZS5OT0RFSlNfMTJfWCxcbiAgICAgIGNvZGU6IGxhbWJkYS5Db2RlLmZyb21Bc3NldCgnbGFtYmRhLWZucycpLFxuICAgICAgaGFuZGxlcjogJ2xhbWJkYS5oYW5kbGVyJywgXG4gICAgICBlbnZpcm9ubWVudDoge1xuICAgICAgICBDSVJDVUlUQlJFQUtFUl9UQUJMRTogdGFibGUudGFibGVOYW1lXG4gICAgICB9XG4gICAgfSk7XG5cbiAgICAvLyBncmFudCB0aGUgbGFtYmRhIHJvbGUgcmVhZC93cml0ZSBwZXJtaXNzaW9ucyB0byBvdXIgdGFibGVcbiAgICB0YWJsZS5ncmFudFJlYWRXcml0ZURhdGEodW5yZWxpYWJsZUxhbWJkYSk7XG5cbiAgICAvLyBkZWZpbmVzIGFuIEFQSSBHYXRld2F5IEh0dHAgQVBJIHJlc291cmNlIGJhY2tlZCBieSBvdXIgXCJkeW5hbW9MYW1iZGFcIiBmdW5jdGlvbi5cbiAgICBsZXQgYXBpID0gbmV3IGFwaWd3Lkh0dHBBcGkodGhpcywgJ0NpcmN1aXRCcmVha2VyR2F0ZXdheScsIHtcbiAgICAgIGRlZmF1bHRJbnRlZ3JhdGlvbjogbmV3IGFwaWd3LkxhbWJkYVByb3h5SW50ZWdyYXRpb24oe1xuICAgICAgICBoYW5kbGVyOiB1bnJlbGlhYmxlTGFtYmRhXG4gICAgICB9KVxuICAgIH0pO1xuXG4gICBuZXcgY2RrLkNmbk91dHB1dCh0aGlzLCAnSFRUUCBBUEkgVXJsJywge1xuICAgICB2YWx1ZTogYXBpLnVybCA/PyAnU29tZXRoaW5nIHdlbnQgd3Jvbmcgd2l0aCB0aGUgZGVwbG95J1xuICAgfSk7XG4gIH1cbn1cbiJdfQ==