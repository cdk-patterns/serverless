import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheEventbridgeAtm = require('../lib/the-eventbridge-atm-stack');

test('Publisher Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeAtm.TheEventbridgeAtmStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "handler.lambdaHandler",
    "Runtime": "nodejs12.x"
    }
  ));
});

test('Consumer 1 Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeAtm.TheEventbridgeAtmStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "handler.case1Handler",
    "Runtime": "nodejs12.x"
    }
  ));
});

test('Consumer 1 Rule Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeAtm.TheEventbridgeAtmStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Events::Rule", {
    "Description": "Approved transactions",
    "EventPattern": {
      "source": [
        "custom.myATMapp"
      ],
      "detail-type": [
        "transaction"
      ],
      "detail": {
        "result": [
          "approved"
        ]
      }
    },
    "State": "ENABLED"
    }
  ));
});

test('Consumer 2 Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeAtm.TheEventbridgeAtmStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "handler.case2Handler",
    "Runtime": "nodejs12.x"
    }
  ));
});

test('Consumer 2 Rule Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeAtm.TheEventbridgeAtmStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Events::Rule", {
    "EventPattern": {
      "source": [
        "custom.myATMapp"
      ],
      "detail-type": [
        "transaction"
      ],
      "detail": {
        "location": [
          {
            "prefix": "NY-"
          }
        ]
      }
    },
    "State": "ENABLED"
    }
  ));
});

test('Consumer 3 Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeAtm.TheEventbridgeAtmStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "handler.case3Handler",
    "Runtime": "nodejs12.x"
    }
  ));
});

test('Consumer 3 Rule Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeAtm.TheEventbridgeAtmStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Events::Rule", {
    "EventPattern": {
      "source": [
        "custom.myATMapp"
      ],
      "detail-type": [
        "transaction"
      ],
      "detail": {
        "result": [
          {
            "anything-but": "approved"
          }
        ]
      }
    },
    "State": "ENABLED"
    }
  ));
});

test('API Gateway Proxy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeAtm.TheEventbridgeAtmStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "{proxy+}"
  }
  ));
});
