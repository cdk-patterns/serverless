"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const assert_1 = require("@aws-cdk/assert");
const cdk = require("@aws-cdk/core");
const TheSimpleWebservice = require("../lib/the-simple-graphql-service-stack");
test('DynamoDB Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSimpleWebservice.TheSimpleGraphqlServiceStack(app, 'MyTestStack');
    // THEN
    assert_1.expect(stack).to(assert_1.haveResourceLike("AWS::DynamoDB::Table", {
        "KeySchema": [
            {
                "AttributeName": "path",
                "KeyType": "HASH"
            }
        ]
    }));
});
test('DynamoDB Read/Write IAM Policy Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSimpleWebservice.TheSimpleGraphqlServiceStack(app, 'MyTestStack');
    // THEN
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
test('DynamoDB Lambda Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSimpleWebservice.TheSimpleGraphqlServiceStack(app, 'MyTestStack');
    // THEN
    assert_1.expect(stack).to(assert_1.haveResourceLike("AWS::Lambda::Function", {
        "Handler": "lambda.handler",
        "Runtime": "nodejs12.x"
    }));
});
test('API Gateway Proxy Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSimpleWebservice.TheSimpleGraphqlServiceStack(app, 'MyTestStack');
    // THEN
    assert_1.expect(stack).to(assert_1.haveResourceLike("AWS::ApiGateway::Resource", {
        "PathPart": "{proxy+}"
    }));
});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidGhlLXNpbXBsZS13ZWJzZXJ2aWNlLnRlc3QuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyJ0aGUtc2ltcGxlLXdlYnNlcnZpY2UudGVzdC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOztBQUFBLDRDQUFtRztBQUNuRyxxQ0FBcUM7QUFDckMsMEVBQTJFO0FBRTNFLElBQUksQ0FBQyxrQkFBa0IsRUFBRSxHQUFHLEVBQUU7SUFDMUIsTUFBTSxHQUFHLEdBQUcsSUFBSSxHQUFHLENBQUMsR0FBRyxFQUFFLENBQUM7SUFDMUIsT0FBTztJQUNQLE1BQU0sS0FBSyxHQUFHLElBQUksbUJBQW1CLENBQUMsd0JBQXdCLENBQUMsR0FBRyxFQUFFLGFBQWEsQ0FBQyxDQUFDO0lBQ25GLE9BQU87SUFDVCxlQUFTLENBQUMsS0FBSyxDQUFDLENBQUMsRUFBRSxDQUFDLHlCQUFnQixDQUFDLHNCQUFzQixFQUFFO1FBQzNELFdBQVcsRUFBRTtZQUNYO2dCQUNFLGVBQWUsRUFBRSxNQUFNO2dCQUN2QixTQUFTLEVBQUUsTUFBTTthQUNsQjtTQUNGO0tBQUMsQ0FDSCxDQUFDLENBQUM7QUFDTCxDQUFDLENBQUMsQ0FBQztBQUVILElBQUksQ0FBQyx3Q0FBd0MsRUFBRSxHQUFHLEVBQUU7SUFDbEQsTUFBTSxHQUFHLEdBQUcsSUFBSSxHQUFHLENBQUMsR0FBRyxFQUFFLENBQUM7SUFDMUIsT0FBTztJQUNQLE1BQU0sS0FBSyxHQUFHLElBQUksbUJBQW1CLENBQUMsd0JBQXdCLENBQUMsR0FBRyxFQUFFLGFBQWEsQ0FBQyxDQUFDO0lBQ25GLE9BQU87SUFDUCxlQUFTLENBQUMsS0FBSyxDQUFDLENBQUMsRUFBRSxDQUFDLHlCQUFnQixDQUFDLGtCQUFrQixFQUFFO1FBQ3ZELGdCQUFnQixFQUFFO1lBQ2hCLFdBQVcsRUFBRTtnQkFDWDtvQkFDQSxRQUFRLEVBQUU7d0JBQ1IsdUJBQXVCO3dCQUN2QixxQkFBcUI7d0JBQ3JCLDJCQUEyQjt3QkFDM0IsZ0JBQWdCO3dCQUNoQixrQkFBa0I7d0JBQ2xCLGVBQWU7d0JBQ2YseUJBQXlCO3dCQUN6QixrQkFBa0I7d0JBQ2xCLHFCQUFxQjt3QkFDckIscUJBQXFCO3FCQUN0QjtvQkFDRCxRQUFRLEVBQUUsT0FBTztpQkFDbEI7YUFBQztTQUNIO0tBQ0YsQ0FDQSxDQUFDLENBQUM7QUFDTCxDQUFDLENBQUMsQ0FBQztBQUVILElBQUksQ0FBQyx5QkFBeUIsRUFBRSxHQUFHLEVBQUU7SUFDbkMsTUFBTSxHQUFHLEdBQUcsSUFBSSxHQUFHLENBQUMsR0FBRyxFQUFFLENBQUM7SUFDMUIsT0FBTztJQUNQLE1BQU0sS0FBSyxHQUFHLElBQUksbUJBQW1CLENBQUMsd0JBQXdCLENBQUMsR0FBRyxFQUFFLGFBQWEsQ0FBQyxDQUFDO0lBQ25GLE9BQU87SUFDUCxlQUFTLENBQUMsS0FBSyxDQUFDLENBQUMsRUFBRSxDQUFDLHlCQUFnQixDQUFDLHVCQUF1QixFQUFFO1FBQzVELFNBQVMsRUFBRSxnQkFBZ0I7UUFDM0IsU0FBUyxFQUFFLFlBQVk7S0FDeEIsQ0FDQSxDQUFDLENBQUM7QUFDTCxDQUFDLENBQUMsQ0FBQztBQUVILElBQUksQ0FBQywyQkFBMkIsRUFBRSxHQUFHLEVBQUU7SUFDckMsTUFBTSxHQUFHLEdBQUcsSUFBSSxHQUFHLENBQUMsR0FBRyxFQUFFLENBQUM7SUFDMUIsT0FBTztJQUNQLE1BQU0sS0FBSyxHQUFHLElBQUksbUJBQW1CLENBQUMsd0JBQXdCLENBQUMsR0FBRyxFQUFFLGFBQWEsQ0FBQyxDQUFDO0lBQ25GLE9BQU87SUFDUCxlQUFTLENBQUMsS0FBSyxDQUFDLENBQUMsRUFBRSxDQUFDLHlCQUFnQixDQUFDLDJCQUEyQixFQUFFO1FBQ2hFLFVBQVUsRUFBRSxVQUFVO0tBQ3ZCLENBQ0EsQ0FBQyxDQUFDO0FBQ0wsQ0FBQyxDQUFDLENBQUMiLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgeyBleHBlY3QgYXMgZXhwZWN0Q0RLLCBtYXRjaFRlbXBsYXRlLCBoYXZlUmVzb3VyY2VMaWtlLCBNYXRjaFN0eWxlIH0gZnJvbSAnQGF3cy1jZGsvYXNzZXJ0JztcbmltcG9ydCAqIGFzIGNkayBmcm9tICdAYXdzLWNkay9jb3JlJztcbmltcG9ydCBUaGVTaW1wbGVXZWJzZXJ2aWNlID0gcmVxdWlyZSgnLi4vbGliL3RoZS1zaW1wbGUtd2Vic2VydmljZS1zdGFjaycpO1xuXG50ZXN0KCdEeW5hbW9EQiBDcmVhdGVkJywgKCkgPT4ge1xuICAgIGNvbnN0IGFwcCA9IG5ldyBjZGsuQXBwKCk7XG4gICAgLy8gV0hFTlxuICAgIGNvbnN0IHN0YWNrID0gbmV3IFRoZVNpbXBsZVdlYnNlcnZpY2UuVGhlU2ltcGxlV2Vic2VydmljZVN0YWNrKGFwcCwgJ015VGVzdFN0YWNrJyk7XG4gICAgLy8gVEhFTlxuICBleHBlY3RDREsoc3RhY2spLnRvKGhhdmVSZXNvdXJjZUxpa2UoXCJBV1M6OkR5bmFtb0RCOjpUYWJsZVwiLCB7XG4gICAgXCJLZXlTY2hlbWFcIjogW1xuICAgICAge1xuICAgICAgICBcIkF0dHJpYnV0ZU5hbWVcIjogXCJwYXRoXCIsXG4gICAgICAgIFwiS2V5VHlwZVwiOiBcIkhBU0hcIlxuICAgICAgfVxuICAgIF19XG4gICkpO1xufSk7XG5cbnRlc3QoJ0R5bmFtb0RCIFJlYWQvV3JpdGUgSUFNIFBvbGljeSBDcmVhdGVkJywgKCkgPT4ge1xuICBjb25zdCBhcHAgPSBuZXcgY2RrLkFwcCgpO1xuICAvLyBXSEVOXG4gIGNvbnN0IHN0YWNrID0gbmV3IFRoZVNpbXBsZVdlYnNlcnZpY2UuVGhlU2ltcGxlV2Vic2VydmljZVN0YWNrKGFwcCwgJ015VGVzdFN0YWNrJyk7XG4gIC8vIFRIRU5cbiAgZXhwZWN0Q0RLKHN0YWNrKS50byhoYXZlUmVzb3VyY2VMaWtlKFwiQVdTOjpJQU06OlBvbGljeVwiLCB7XG4gICAgXCJQb2xpY3lEb2N1bWVudFwiOiB7XG4gICAgICBcIlN0YXRlbWVudFwiOiBbXG4gICAgICAgIHtcbiAgICAgICAgXCJBY3Rpb25cIjogW1xuICAgICAgICAgIFwiZHluYW1vZGI6QmF0Y2hHZXRJdGVtXCIsXG4gICAgICAgICAgXCJkeW5hbW9kYjpHZXRSZWNvcmRzXCIsXG4gICAgICAgICAgXCJkeW5hbW9kYjpHZXRTaGFyZEl0ZXJhdG9yXCIsXG4gICAgICAgICAgXCJkeW5hbW9kYjpRdWVyeVwiLFxuICAgICAgICAgIFwiZHluYW1vZGI6R2V0SXRlbVwiLFxuICAgICAgICAgIFwiZHluYW1vZGI6U2NhblwiLFxuICAgICAgICAgIFwiZHluYW1vZGI6QmF0Y2hXcml0ZUl0ZW1cIixcbiAgICAgICAgICBcImR5bmFtb2RiOlB1dEl0ZW1cIixcbiAgICAgICAgICBcImR5bmFtb2RiOlVwZGF0ZUl0ZW1cIixcbiAgICAgICAgICBcImR5bmFtb2RiOkRlbGV0ZUl0ZW1cIlxuICAgICAgICBdLFxuICAgICAgICBcIkVmZmVjdFwiOiBcIkFsbG93XCIgIFxuICAgICAgfV1cbiAgICB9XG4gIH1cbiAgKSk7XG59KTtcblxudGVzdCgnRHluYW1vREIgTGFtYmRhIENyZWF0ZWQnLCAoKSA9PiB7XG4gIGNvbnN0IGFwcCA9IG5ldyBjZGsuQXBwKCk7XG4gIC8vIFdIRU5cbiAgY29uc3Qgc3RhY2sgPSBuZXcgVGhlU2ltcGxlV2Vic2VydmljZS5UaGVTaW1wbGVXZWJzZXJ2aWNlU3RhY2soYXBwLCAnTXlUZXN0U3RhY2snKTtcbiAgLy8gVEhFTlxuICBleHBlY3RDREsoc3RhY2spLnRvKGhhdmVSZXNvdXJjZUxpa2UoXCJBV1M6OkxhbWJkYTo6RnVuY3Rpb25cIiwge1xuICAgIFwiSGFuZGxlclwiOiBcImxhbWJkYS5oYW5kbGVyXCIsXG4gICAgXCJSdW50aW1lXCI6IFwibm9kZWpzMTIueFwiXG4gIH1cbiAgKSk7XG59KTtcblxudGVzdCgnQVBJIEdhdGV3YXkgUHJveHkgQ3JlYXRlZCcsICgpID0+IHtcbiAgY29uc3QgYXBwID0gbmV3IGNkay5BcHAoKTtcbiAgLy8gV0hFTlxuICBjb25zdCBzdGFjayA9IG5ldyBUaGVTaW1wbGVXZWJzZXJ2aWNlLlRoZVNpbXBsZVdlYnNlcnZpY2VTdGFjayhhcHAsICdNeVRlc3RTdGFjaycpO1xuICAvLyBUSEVOXG4gIGV4cGVjdENESyhzdGFjaykudG8oaGF2ZVJlc291cmNlTGlrZShcIkFXUzo6QXBpR2F0ZXdheTo6UmVzb3VyY2VcIiwge1xuICAgIFwiUGF0aFBhcnRcIjogXCJ7cHJveHkrfVwiXG4gIH1cbiAgKSk7XG59KTtcbiJdfQ==