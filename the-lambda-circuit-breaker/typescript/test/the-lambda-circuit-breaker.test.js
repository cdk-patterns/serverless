"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const assert_1 = require("@aws-cdk/assert");
const cdk = require("@aws-cdk/core");
const TheLambdaCircuitBreaker = require("../lib/the-lambda-circuit-breaker-stack");
let stack;
beforeAll(() => {
    const app = new cdk.App();
    // WHEN
    stack = new TheLambdaCircuitBreaker.TheLambdaCircuitBreakerStack(app, 'MyTestStack');
});
test('DynamoDB Created', () => {
    assert_1.expect(stack).to(assert_1.haveResourceLike("AWS::DynamoDB::Table", {
        "KeySchema": [
            {
                "AttributeName": "id",
                "KeyType": "HASH"
            }
        ]
    }));
});
test('DynamoDB Read/Write IAM Policy Created', () => {
    assert_1.expect(stack).to(assert_1.haveResourceLike("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": [
                {
                    "Action": [
                        "dynamodb:BatchGetItem",
                        "dynamodb:GetRecords",
                        "dynamodb:GetShardIterator",
                        "dynamodb:Query",
                        "dynamodb:GetItem",
                        "dynamodb:Scan",
                        "dynamodb:BatchWriteItem",
                        "dynamodb:PutItem",
                        "dynamodb:UpdateItem",
                        "dynamodb:DeleteItem"
                    ],
                    "Effect": "Allow"
                }
            ]
        }
    }));
});
test('Circuit Breaker Lambda Created', () => {
    assert_1.expect(stack).to(assert_1.haveResourceLike("AWS::Lambda::Function", {
        "Handler": "unreliable.handler",
        "Runtime": "nodejs12.x"
    }));
});
test('API Gateway Http API Created', () => {
    assert_1.expect(stack).to(assert_1.haveResourceLike("AWS::ApiGatewayV2::Api", {
        "ProtocolType": "HTTP"
    }));
});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidGhlLWxhbWJkYS1jaXJjdWl0LWJyZWFrZXIudGVzdC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbInRoZS1sYW1iZGEtY2lyY3VpdC1icmVha2VyLnRlc3QudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7QUFBQSw0Q0FBa0c7QUFDbEcscUNBQXFDO0FBQ3JDLG1GQUFtRjtBQUVuRixJQUFJLEtBQTBELENBQUM7QUFFL0QsU0FBUyxDQUFDLEdBQUcsRUFBRTtJQUNiLE1BQU0sR0FBRyxHQUFHLElBQUksR0FBRyxDQUFDLEdBQUcsRUFBRSxDQUFDO0lBQzFCLE9BQU87SUFDUCxLQUFLLEdBQUcsSUFBSSx1QkFBdUIsQ0FBQyw0QkFBNEIsQ0FBQyxHQUFHLEVBQUUsYUFBYSxDQUFDLENBQUM7QUFDdkYsQ0FBQyxDQUFDLENBQUM7QUFFSCxJQUFJLENBQUMsa0JBQWtCLEVBQUUsR0FBRyxFQUFFO0lBQzVCLGVBQVMsQ0FBQyxLQUFLLENBQUMsQ0FBQyxFQUFFLENBQUMseUJBQWdCLENBQUMsc0JBQXNCLEVBQUU7UUFDM0QsV0FBVyxFQUFFO1lBQ1g7Z0JBQ0UsZUFBZSxFQUFFLElBQUk7Z0JBQ3JCLFNBQVMsRUFBRSxNQUFNO2FBQ2xCO1NBQ0Y7S0FBQyxDQUNILENBQUMsQ0FBQztBQUNMLENBQUMsQ0FBQyxDQUFDO0FBRUgsSUFBSSxDQUFDLHdDQUF3QyxFQUFFLEdBQUcsRUFBRTtJQUNsRCxlQUFTLENBQUMsS0FBSyxDQUFDLENBQUMsRUFBRSxDQUFDLHlCQUFnQixDQUFDLGtCQUFrQixFQUFFO1FBQ3ZELGdCQUFnQixFQUFFO1lBQ2hCLFdBQVcsRUFBRTtnQkFDWDtvQkFDQSxRQUFRLEVBQUU7d0JBQ1IsdUJBQXVCO3dCQUN2QixxQkFBcUI7d0JBQ3JCLDJCQUEyQjt3QkFDM0IsZ0JBQWdCO3dCQUNoQixrQkFBa0I7d0JBQ2xCLGVBQWU7d0JBQ2YseUJBQXlCO3dCQUN6QixrQkFBa0I7d0JBQ2xCLHFCQUFxQjt3QkFDckIscUJBQXFCO3FCQUN0QjtvQkFDRCxRQUFRLEVBQUUsT0FBTztpQkFDbEI7YUFBQztTQUNIO0tBQ0YsQ0FDQSxDQUFDLENBQUM7QUFDTCxDQUFDLENBQUMsQ0FBQztBQUVILElBQUksQ0FBQyxnQ0FBZ0MsRUFBRSxHQUFHLEVBQUU7SUFDMUMsZUFBUyxDQUFDLEtBQUssQ0FBQyxDQUFDLEVBQUUsQ0FBQyx5QkFBZ0IsQ0FBQyx1QkFBdUIsRUFBRTtRQUM1RCxTQUFTLEVBQUUsb0JBQW9CO1FBQy9CLFNBQVMsRUFBRSxZQUFZO0tBQ3hCLENBQ0EsQ0FBQyxDQUFDO0FBQ0wsQ0FBQyxDQUFDLENBQUM7QUFFSCxJQUFJLENBQUMsOEJBQThCLEVBQUUsR0FBRyxFQUFFO0lBQ3hDLGVBQVMsQ0FBQyxLQUFLLENBQUMsQ0FBQyxFQUFFLENBQUMseUJBQWdCLENBQUMsd0JBQXdCLEVBQUU7UUFDN0QsY0FBYyxFQUFFLE1BQU07S0FDdkIsQ0FDQSxDQUFDLENBQUM7QUFDTCxDQUFDLENBQUMsQ0FBQyIsInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB7IGV4cGVjdCBhcyBleHBlY3RDREssIG1hdGNoVGVtcGxhdGUsIGhhdmVSZXNvdXJjZUxpa2UsTWF0Y2hTdHlsZSB9IGZyb20gJ0Bhd3MtY2RrL2Fzc2VydCc7XG5pbXBvcnQgKiBhcyBjZGsgZnJvbSAnQGF3cy1jZGsvY29yZSc7XG5pbXBvcnQgKiBhcyBUaGVMYW1iZGFDaXJjdWl0QnJlYWtlciBmcm9tICcuLi9saWIvdGhlLWxhbWJkYS1jaXJjdWl0LWJyZWFrZXItc3RhY2snO1xuXG5sZXQgc3RhY2s6VGhlTGFtYmRhQ2lyY3VpdEJyZWFrZXIuVGhlTGFtYmRhQ2lyY3VpdEJyZWFrZXJTdGFjaztcblxuYmVmb3JlQWxsKCgpID0+IHtcbiAgY29uc3QgYXBwID0gbmV3IGNkay5BcHAoKTtcbiAgLy8gV0hFTlxuICBzdGFjayA9IG5ldyBUaGVMYW1iZGFDaXJjdWl0QnJlYWtlci5UaGVMYW1iZGFDaXJjdWl0QnJlYWtlclN0YWNrKGFwcCwgJ015VGVzdFN0YWNrJyk7XG59KTtcblxudGVzdCgnRHluYW1vREIgQ3JlYXRlZCcsICgpID0+IHtcbiAgZXhwZWN0Q0RLKHN0YWNrKS50byhoYXZlUmVzb3VyY2VMaWtlKFwiQVdTOjpEeW5hbW9EQjo6VGFibGVcIiwge1xuICAgIFwiS2V5U2NoZW1hXCI6IFtcbiAgICAgIHtcbiAgICAgICAgXCJBdHRyaWJ1dGVOYW1lXCI6IFwiaWRcIixcbiAgICAgICAgXCJLZXlUeXBlXCI6IFwiSEFTSFwiXG4gICAgICB9XG4gICAgXX1cbiAgKSk7XG59KTtcblxudGVzdCgnRHluYW1vREIgUmVhZC9Xcml0ZSBJQU0gUG9saWN5IENyZWF0ZWQnLCAoKSA9PiB7XG4gIGV4cGVjdENESyhzdGFjaykudG8oaGF2ZVJlc291cmNlTGlrZShcIkFXUzo6SUFNOjpQb2xpY3lcIiwge1xuICAgIFwiUG9saWN5RG9jdW1lbnRcIjoge1xuICAgICAgXCJTdGF0ZW1lbnRcIjogW1xuICAgICAgICB7XG4gICAgICAgIFwiQWN0aW9uXCI6IFtcbiAgICAgICAgICBcImR5bmFtb2RiOkJhdGNoR2V0SXRlbVwiLFxuICAgICAgICAgIFwiZHluYW1vZGI6R2V0UmVjb3Jkc1wiLFxuICAgICAgICAgIFwiZHluYW1vZGI6R2V0U2hhcmRJdGVyYXRvclwiLFxuICAgICAgICAgIFwiZHluYW1vZGI6UXVlcnlcIixcbiAgICAgICAgICBcImR5bmFtb2RiOkdldEl0ZW1cIixcbiAgICAgICAgICBcImR5bmFtb2RiOlNjYW5cIixcbiAgICAgICAgICBcImR5bmFtb2RiOkJhdGNoV3JpdGVJdGVtXCIsXG4gICAgICAgICAgXCJkeW5hbW9kYjpQdXRJdGVtXCIsXG4gICAgICAgICAgXCJkeW5hbW9kYjpVcGRhdGVJdGVtXCIsXG4gICAgICAgICAgXCJkeW5hbW9kYjpEZWxldGVJdGVtXCJcbiAgICAgICAgXSxcbiAgICAgICAgXCJFZmZlY3RcIjogXCJBbGxvd1wiICBcbiAgICAgIH1dXG4gICAgfVxuICB9XG4gICkpO1xufSk7XG5cbnRlc3QoJ0NpcmN1aXQgQnJlYWtlciBMYW1iZGEgQ3JlYXRlZCcsICgpID0+IHtcbiAgZXhwZWN0Q0RLKHN0YWNrKS50byhoYXZlUmVzb3VyY2VMaWtlKFwiQVdTOjpMYW1iZGE6OkZ1bmN0aW9uXCIsIHtcbiAgICBcIkhhbmRsZXJcIjogXCJ1bnJlbGlhYmxlLmhhbmRsZXJcIixcbiAgICBcIlJ1bnRpbWVcIjogXCJub2RlanMxMi54XCJcbiAgfVxuICApKTtcbn0pO1xuXG50ZXN0KCdBUEkgR2F0ZXdheSBIdHRwIEFQSSBDcmVhdGVkJywgKCkgPT4ge1xuICBleHBlY3RDREsoc3RhY2spLnRvKGhhdmVSZXNvdXJjZUxpa2UoXCJBV1M6OkFwaUdhdGV3YXlWMjo6QXBpXCIsIHtcbiAgICBcIlByb3RvY29sVHlwZVwiOiBcIkhUVFBcIlxuICB9XG4gICkpO1xufSk7XG4iXX0=