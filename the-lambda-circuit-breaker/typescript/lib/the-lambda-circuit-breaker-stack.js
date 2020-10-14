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
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidGhlLWxhbWJkYS1jaXJjdWl0LWJyZWFrZXItc3RhY2suanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyJ0aGUtbGFtYmRhLWNpcmN1aXQtYnJlYWtlci1zdGFjay50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7QUFBQSxxQ0FBcUM7QUFDckMscURBQXNEO0FBQ3RELGtEQUFtRDtBQUNuRCxtREFBb0Q7QUFDcEQsTUFBTSxJQUFJLEdBQUcsT0FBTyxDQUFDLE1BQU0sQ0FBQyxDQUFDO0FBRTdCLE1BQWEsNEJBQTZCLFNBQVEsR0FBRyxDQUFDLEtBQUs7SUFDekQsWUFBWSxLQUFvQixFQUFFLEVBQVUsRUFBRSxLQUFzQjs7UUFDbEUsS0FBSyxDQUFDLEtBQUssRUFBRSxFQUFFLEVBQUUsS0FBSyxDQUFDLENBQUM7UUFFeEIsNkNBQTZDO1FBQzdDLE1BQU0sS0FBSyxHQUFHLElBQUksUUFBUSxDQUFDLEtBQUssQ0FBQyxJQUFJLEVBQUUscUJBQXFCLEVBQUU7WUFDNUQsWUFBWSxFQUFFLEVBQUUsSUFBSSxFQUFFLElBQUksRUFBRSxJQUFJLEVBQUUsUUFBUSxDQUFDLGFBQWEsQ0FBQyxNQUFNLEVBQUU7WUFDakUsYUFBYSxFQUFFLEdBQUcsQ0FBQyxhQUFhLENBQUMsT0FBTztTQUN6QyxDQUFDLENBQUM7UUFFSCxnREFBZ0Q7UUFDaEQsTUFBTSxnQkFBZ0IsR0FBRyxJQUFJLE1BQU0sQ0FBQyxjQUFjLENBQUMsSUFBSSxFQUFFLHlCQUF5QixFQUFFO1lBQ2xGLEtBQUssRUFBRSxJQUFJLENBQUMsSUFBSSxDQUFDLFNBQVMsRUFBRSw2QkFBNkIsQ0FBQztZQUMxRCxPQUFPLEVBQUUsU0FBUztZQUNsQixXQUFXLEVBQUU7Z0JBQ1gsb0JBQW9CLEVBQUUsS0FBSyxDQUFDLFNBQVM7YUFDdEM7U0FDRixDQUFDLENBQUM7UUFFSCw0REFBNEQ7UUFDNUQsS0FBSyxDQUFDLGtCQUFrQixDQUFDLGdCQUFnQixDQUFDLENBQUM7UUFFM0Msa0ZBQWtGO1FBQ2xGLElBQUksR0FBRyxHQUFHLElBQUksS0FBSyxDQUFDLE9BQU8sQ0FBQyxJQUFJLEVBQUUsdUJBQXVCLEVBQUU7WUFDekQsa0JBQWtCLEVBQUUsSUFBSSxLQUFLLENBQUMsc0JBQXNCLENBQUM7Z0JBQ25ELE9BQU8sRUFBRSxnQkFBZ0I7YUFDMUIsQ0FBQztTQUNILENBQUMsQ0FBQztRQUVKLElBQUksR0FBRyxDQUFDLFNBQVMsQ0FBQyxJQUFJLEVBQUUsY0FBYyxFQUFFO1lBQ3RDLEtBQUssUUFBRSxHQUFHLENBQUMsR0FBRyxtQ0FBSSxzQ0FBc0M7U0FDekQsQ0FBQyxDQUFDO0lBQ0osQ0FBQztDQUNGO0FBakNELG9FQWlDQyIsInNvdXJjZXNDb250ZW50IjpbImltcG9ydCAqIGFzIGNkayBmcm9tICdAYXdzLWNkay9jb3JlJztcbmltcG9ydCBsYW1iZGEgPSByZXF1aXJlKCdAYXdzLWNkay9hd3MtbGFtYmRhLW5vZGVqcycpO1xuaW1wb3J0IGR5bmFtb2RiID0gcmVxdWlyZSgnQGF3cy1jZGsvYXdzLWR5bmFtb2RiJyk7XG5pbXBvcnQgYXBpZ3cgPSByZXF1aXJlKCdAYXdzLWNkay9hd3MtYXBpZ2F0ZXdheXYyJyk7XG5jb25zdCBwYXRoID0gcmVxdWlyZSgncGF0aCcpO1xuXG5leHBvcnQgY2xhc3MgVGhlTGFtYmRhQ2lyY3VpdEJyZWFrZXJTdGFjayBleHRlbmRzIGNkay5TdGFjayB7XG4gIGNvbnN0cnVjdG9yKHNjb3BlOiBjZGsuQ29uc3RydWN0LCBpZDogc3RyaW5nLCBwcm9wcz86IGNkay5TdGFja1Byb3BzKSB7XG4gICAgc3VwZXIoc2NvcGUsIGlkLCBwcm9wcyk7XG5cbiAgICAvL0R5bmFtb0RCIFRhYmxlIFRvIEhvbGQgQ2lyY3VpdGJyZWFrZXIgU3RhdGVcbiAgICBjb25zdCB0YWJsZSA9IG5ldyBkeW5hbW9kYi5UYWJsZSh0aGlzLCAnQ2lyY3VpdEJyZWFrZXJUYWJsZScsIHtcbiAgICAgIHBhcnRpdGlvbktleTogeyBuYW1lOiAnaWQnLCB0eXBlOiBkeW5hbW9kYi5BdHRyaWJ1dGVUeXBlLlNUUklORyB9LFxuICAgICAgcmVtb3ZhbFBvbGljeTogY2RrLlJlbW92YWxQb2xpY3kuREVTVFJPWVxuICAgIH0pO1xuXG4gICAgLy8gQ3JlYXRlIGEgTGFtYmRhIEZ1bmN0aW9uIHdpdGggdW5yZWxpYWJsZSBjb2RlXG4gICAgY29uc3QgdW5yZWxpYWJsZUxhbWJkYSA9IG5ldyBsYW1iZGEuTm9kZWpzRnVuY3Rpb24odGhpcywgJ1VucmVsaWFibGVMYW1iZGFIYW5kbGVyJywge1xuICAgICAgZW50cnk6IHBhdGguam9pbihfX2Rpcm5hbWUsICcuLi9sYW1iZGEtZm5zL3VucmVsaWFibGUudHMnKSxcbiAgICAgIGhhbmRsZXI6ICdoYW5kbGVyJyxcbiAgICAgIGVudmlyb25tZW50OiB7XG4gICAgICAgIENJUkNVSVRCUkVBS0VSX1RBQkxFOiB0YWJsZS50YWJsZU5hbWVcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIC8vIGdyYW50IHRoZSBsYW1iZGEgcm9sZSByZWFkL3dyaXRlIHBlcm1pc3Npb25zIHRvIG91ciB0YWJsZVxuICAgIHRhYmxlLmdyYW50UmVhZFdyaXRlRGF0YSh1bnJlbGlhYmxlTGFtYmRhKTtcblxuICAgIC8vIGRlZmluZXMgYW4gQVBJIEdhdGV3YXkgSHR0cCBBUEkgcmVzb3VyY2UgYmFja2VkIGJ5IG91ciBcImR5bmFtb0xhbWJkYVwiIGZ1bmN0aW9uLlxuICAgIGxldCBhcGkgPSBuZXcgYXBpZ3cuSHR0cEFwaSh0aGlzLCAnQ2lyY3VpdEJyZWFrZXJHYXRld2F5Jywge1xuICAgICAgZGVmYXVsdEludGVncmF0aW9uOiBuZXcgYXBpZ3cuTGFtYmRhUHJveHlJbnRlZ3JhdGlvbih7XG4gICAgICAgIGhhbmRsZXI6IHVucmVsaWFibGVMYW1iZGFcbiAgICAgIH0pXG4gICAgfSk7XG5cbiAgIG5ldyBjZGsuQ2ZuT3V0cHV0KHRoaXMsICdIVFRQIEFQSSBVcmwnLCB7XG4gICAgIHZhbHVlOiBhcGkudXJsID8/ICdTb21ldGhpbmcgd2VudCB3cm9uZyB3aXRoIHRoZSBkZXBsb3knXG4gICB9KTtcbiAgfVxufVxuIl19