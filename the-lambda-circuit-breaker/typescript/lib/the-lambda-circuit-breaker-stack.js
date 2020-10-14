"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TheLambdaCircuitBreakerStack = void 0;
const cdk = require("@aws-cdk/core");
const lambda = require("@aws-cdk/aws-lambda-nodejs");
const dynamodb = require("@aws-cdk/aws-dynamodb");
const apigw = require("@aws-cdk/aws-apigatewayv2");
const path = require('path');
class TheLambdaCircuitBreakerStack extends cdk.Stack {
    constructor(scope, id, props) {
        var _a;
        super(scope, id, props);
        //DynamoDB Table To Hold Circuitbreaker State
        const table = new dynamodb.Table(this, 'CircuitBreakerTable', {
            partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
            removalPolicy: cdk.RemovalPolicy.DESTROY
        });
        // Create a Lambda Function with unreliable code
        /*const unreliableLambda = new lambda.Function(this, 'UnreliableLambdaHandler', {
          runtime: lambda.Runtime.NODEJS_12_X,
          code: lambda.Code.fromAsset('lambda-fns'),
          handler: 'unreliable.handler',
          environment: {
            CIRCUITBREAKER_TABLE: table.tableName
          }
        });*/
        const unreliableLambda = new lambda.NodejsFunction(this, 'UnreliableLambdaHandler', {
            entry: path.join(__dirname, '../lambda-fns/unreliable.ts'),
            handler: 'handler',
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
            value: (_a = api.url) !== null && _a !== void 0 ? _a : 'Something went wrong with the deploy'
        });
    }
}
exports.TheLambdaCircuitBreakerStack = TheLambdaCircuitBreakerStack;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidGhlLWxhbWJkYS1jaXJjdWl0LWJyZWFrZXItc3RhY2suanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyJ0aGUtbGFtYmRhLWNpcmN1aXQtYnJlYWtlci1zdGFjay50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7QUFBQSxxQ0FBcUM7QUFDckMscURBQXNEO0FBQ3RELGtEQUFtRDtBQUNuRCxtREFBb0Q7QUFDcEQsTUFBTSxJQUFJLEdBQUcsT0FBTyxDQUFDLE1BQU0sQ0FBQyxDQUFDO0FBRTdCLE1BQWEsNEJBQTZCLFNBQVEsR0FBRyxDQUFDLEtBQUs7SUFDekQsWUFBWSxLQUFvQixFQUFFLEVBQVUsRUFBRSxLQUFzQjs7UUFDbEUsS0FBSyxDQUFDLEtBQUssRUFBRSxFQUFFLEVBQUUsS0FBSyxDQUFDLENBQUM7UUFFeEIsNkNBQTZDO1FBQzdDLE1BQU0sS0FBSyxHQUFHLElBQUksUUFBUSxDQUFDLEtBQUssQ0FBQyxJQUFJLEVBQUUscUJBQXFCLEVBQUU7WUFDNUQsWUFBWSxFQUFFLEVBQUUsSUFBSSxFQUFFLElBQUksRUFBRSxJQUFJLEVBQUUsUUFBUSxDQUFDLGFBQWEsQ0FBQyxNQUFNLEVBQUU7WUFDakUsYUFBYSxFQUFFLEdBQUcsQ0FBQyxhQUFhLENBQUMsT0FBTztTQUN6QyxDQUFDLENBQUM7UUFFSCxnREFBZ0Q7UUFDaEQ7Ozs7Ozs7YUFPSztRQUNMLE1BQU0sZ0JBQWdCLEdBQUcsSUFBSSxNQUFNLENBQUMsY0FBYyxDQUFDLElBQUksRUFBRSx5QkFBeUIsRUFBRTtZQUNsRixLQUFLLEVBQUUsSUFBSSxDQUFDLElBQUksQ0FBQyxTQUFTLEVBQUUsNkJBQTZCLENBQUM7WUFDMUQsT0FBTyxFQUFFLFNBQVM7WUFDbEIsV0FBVyxFQUFFO2dCQUNYLG9CQUFvQixFQUFFLEtBQUssQ0FBQyxTQUFTO2FBQ3RDO1NBQ0YsQ0FBQyxDQUFDO1FBRUgsNERBQTREO1FBQzVELEtBQUssQ0FBQyxrQkFBa0IsQ0FBQyxnQkFBZ0IsQ0FBQyxDQUFDO1FBRTNDLGtGQUFrRjtRQUNsRixJQUFJLEdBQUcsR0FBRyxJQUFJLEtBQUssQ0FBQyxPQUFPLENBQUMsSUFBSSxFQUFFLHVCQUF1QixFQUFFO1lBQ3pELGtCQUFrQixFQUFFLElBQUksS0FBSyxDQUFDLHNCQUFzQixDQUFDO2dCQUNuRCxPQUFPLEVBQUUsZ0JBQWdCO2FBQzFCLENBQUM7U0FDSCxDQUFDLENBQUM7UUFFSixJQUFJLEdBQUcsQ0FBQyxTQUFTLENBQUMsSUFBSSxFQUFFLGNBQWMsRUFBRTtZQUN0QyxLQUFLLFFBQUUsR0FBRyxDQUFDLEdBQUcsbUNBQUksc0NBQXNDO1NBQ3pELENBQUMsQ0FBQztJQUNKLENBQUM7Q0FDRjtBQXpDRCxvRUF5Q0MiLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBjZGsgZnJvbSAnQGF3cy1jZGsvY29yZSc7XG5pbXBvcnQgbGFtYmRhID0gcmVxdWlyZSgnQGF3cy1jZGsvYXdzLWxhbWJkYS1ub2RlanMnKTtcbmltcG9ydCBkeW5hbW9kYiA9IHJlcXVpcmUoJ0Bhd3MtY2RrL2F3cy1keW5hbW9kYicpO1xuaW1wb3J0IGFwaWd3ID0gcmVxdWlyZSgnQGF3cy1jZGsvYXdzLWFwaWdhdGV3YXl2MicpO1xuY29uc3QgcGF0aCA9IHJlcXVpcmUoJ3BhdGgnKTtcblxuZXhwb3J0IGNsYXNzIFRoZUxhbWJkYUNpcmN1aXRCcmVha2VyU3RhY2sgZXh0ZW5kcyBjZGsuU3RhY2sge1xuICBjb25zdHJ1Y3RvcihzY29wZTogY2RrLkNvbnN0cnVjdCwgaWQ6IHN0cmluZywgcHJvcHM/OiBjZGsuU3RhY2tQcm9wcykge1xuICAgIHN1cGVyKHNjb3BlLCBpZCwgcHJvcHMpO1xuXG4gICAgLy9EeW5hbW9EQiBUYWJsZSBUbyBIb2xkIENpcmN1aXRicmVha2VyIFN0YXRlXG4gICAgY29uc3QgdGFibGUgPSBuZXcgZHluYW1vZGIuVGFibGUodGhpcywgJ0NpcmN1aXRCcmVha2VyVGFibGUnLCB7XG4gICAgICBwYXJ0aXRpb25LZXk6IHsgbmFtZTogJ2lkJywgdHlwZTogZHluYW1vZGIuQXR0cmlidXRlVHlwZS5TVFJJTkcgfSxcbiAgICAgIHJlbW92YWxQb2xpY3k6IGNkay5SZW1vdmFsUG9saWN5LkRFU1RST1lcbiAgICB9KTtcblxuICAgIC8vIENyZWF0ZSBhIExhbWJkYSBGdW5jdGlvbiB3aXRoIHVucmVsaWFibGUgY29kZVxuICAgIC8qY29uc3QgdW5yZWxpYWJsZUxhbWJkYSA9IG5ldyBsYW1iZGEuRnVuY3Rpb24odGhpcywgJ1VucmVsaWFibGVMYW1iZGFIYW5kbGVyJywge1xuICAgICAgcnVudGltZTogbGFtYmRhLlJ1bnRpbWUuTk9ERUpTXzEyX1gsXG4gICAgICBjb2RlOiBsYW1iZGEuQ29kZS5mcm9tQXNzZXQoJ2xhbWJkYS1mbnMnKSwgXG4gICAgICBoYW5kbGVyOiAndW5yZWxpYWJsZS5oYW5kbGVyJywgXG4gICAgICBlbnZpcm9ubWVudDoge1xuICAgICAgICBDSVJDVUlUQlJFQUtFUl9UQUJMRTogdGFibGUudGFibGVOYW1lXG4gICAgICB9XG4gICAgfSk7Ki9cbiAgICBjb25zdCB1bnJlbGlhYmxlTGFtYmRhID0gbmV3IGxhbWJkYS5Ob2RlanNGdW5jdGlvbih0aGlzLCAnVW5yZWxpYWJsZUxhbWJkYUhhbmRsZXInLCB7XG4gICAgICBlbnRyeTogcGF0aC5qb2luKF9fZGlybmFtZSwgJy4uL2xhbWJkYS1mbnMvdW5yZWxpYWJsZS50cycpLCAvLyBhY2NlcHRzIC5qcywgLmpzeCwgLnRzIGFuZCAudHN4IGZpbGVzXG4gICAgICBoYW5kbGVyOiAnaGFuZGxlcicsXG4gICAgICBlbnZpcm9ubWVudDoge1xuICAgICAgICBDSVJDVUlUQlJFQUtFUl9UQUJMRTogdGFibGUudGFibGVOYW1lXG4gICAgICB9XG4gICAgfSk7XG5cbiAgICAvLyBncmFudCB0aGUgbGFtYmRhIHJvbGUgcmVhZC93cml0ZSBwZXJtaXNzaW9ucyB0byBvdXIgdGFibGVcbiAgICB0YWJsZS5ncmFudFJlYWRXcml0ZURhdGEodW5yZWxpYWJsZUxhbWJkYSk7XG5cbiAgICAvLyBkZWZpbmVzIGFuIEFQSSBHYXRld2F5IEh0dHAgQVBJIHJlc291cmNlIGJhY2tlZCBieSBvdXIgXCJkeW5hbW9MYW1iZGFcIiBmdW5jdGlvbi5cbiAgICBsZXQgYXBpID0gbmV3IGFwaWd3Lkh0dHBBcGkodGhpcywgJ0NpcmN1aXRCcmVha2VyR2F0ZXdheScsIHtcbiAgICAgIGRlZmF1bHRJbnRlZ3JhdGlvbjogbmV3IGFwaWd3LkxhbWJkYVByb3h5SW50ZWdyYXRpb24oe1xuICAgICAgICBoYW5kbGVyOiB1bnJlbGlhYmxlTGFtYmRhXG4gICAgICB9KVxuICAgIH0pO1xuXG4gICBuZXcgY2RrLkNmbk91dHB1dCh0aGlzLCAnSFRUUCBBUEkgVXJsJywge1xuICAgICB2YWx1ZTogYXBpLnVybCA/PyAnU29tZXRoaW5nIHdlbnQgd3Jvbmcgd2l0aCB0aGUgZGVwbG95J1xuICAgfSk7XG4gIH1cbn1cbiJdfQ==