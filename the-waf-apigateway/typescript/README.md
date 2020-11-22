# The Waf API Gateway

![architecture](img/the-waf-apigateway.png)

This is a cdk stack to deploy a simple API gateway, and attach a WAF (Web Application Firewall) from Andrew Frazer (<https://github.com/mrpackethead>).

The apigateway stack creates a trival REST apigateway, with a single method which returns 'hello world!' to a GET request. 
THe WAF stack creates a WAF WebACL and attaches it to the the apigateway. It demonstrates a geo-matching rule, and the use of some AWS managed rulesets. This waf stack could be used for any resource that you can attach a WAF rule to ( Such as a load balancer / Cloudfront distribution etc) simply by passing the resources ARN to the stack. 

Some Useful References:

| Author        | Link           |
| ------------- | ------------- |
| AWS      | [WAF Docs](https://aws.amazon.com/waf/) |
| AWS | [WAF Pricing](https://aws.amazon.com/waf/pricing/) |
| AWS | [Developer Guide](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-awswaf.html) |
| AWS | [Knowledge Center](https://aws.amazon.com/premiumsupport/knowledge-center/waf-block-common-attacks/) |
| AWS Whitepaper | [Guidelines For Implementing WAF](https://d1.awsstatic.com/whitepapers/guidelines-implementing-aws-waf.pdf) |

![AWS Well Architected](img/well_architected.png)

The [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/) Framework helps you understand the pros and cons of
decisions you make while building systems on AWS. By using the Framework, you will learn architectural best practices for designing and operating reliable, secure, efficient, and cost-effective systems in the cloud. It provides a way for you to consistently measure your architectures against best practices and identify areas for improvement.

We believe that having well-architected systems greatly increases the likelihood of business success.

[Serverless Lens Whitepaper](https://d1.awsstatic.com/whitepapers/architecture/AWS-Serverless-Applications-Lens.pdf) <br />
[Well Architected Whitepaper](http://d0.awsstatic.com/whitepapers/architecture/AWS_Well-Architected_Framework.pdf)

### The Security Pillar

<strong>Note -</strong> The content for this section is a subset of the [Serverless Lens Whitepaper](https://d1.awsstatic.com/whitepapers/architecture/AWS-Serverless-Applications-Lens.pdf) with some minor tweaks.

The [security pillar](https://d1.awsstatic.com/whitepapers/architecture/AWS-Serverless-Applications-Lens.pdf#page=38) includes the ability to protect information, systems, and assets while delivering business value through risk assessments and mitigation strategies.

> SEC 1: How do you control access to your Serverless API?

Use authentication and authorization mechanisms to prevent unauthorized access, and enforce quotas for public resources.

Best Practices:

1/ Use appropriate endpoint type and mechanisms to secure access to your API

## What's Included In This Pattern?

After deployment you will have a WebACL setup in front of a regional API Gateway with 4 different rule groups:

- AWSManagedRulesCommonRuleSet
- AWSManagedRulesAnonymousIpList
- AWSManagedRulesAmazonIpReputationList
- GeoBlock NZ from accessing the content

Note all AWS Managed rule groups can be found [here](https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups-list.html)

### AWSManagedRulesCommonRuleSet

Core rule set (CRS)

VendorName: AWS, Name: AWSManagedRulesCommonRuleSet, WCU: 700

The Core rule set (CRS) rule group contains rules that are generally applicable to web applications. This provides protection against exploitation of a wide range of vulnerabilities, including high risk and commonly occurring vulnerabilities described in OWASP publications. Consider using this rule group for any AWS WAF use case.

**Note** that SizeRestrictions_BODY has been excluded in this implementation

### AWSManagedRulesAnonymousIpList

Anonymous IP list

VendorName: AWS, Name: AWSManagedRulesAnonymousIpList, WCU: 50

The Anonymous IP list rule group contains rules to block requests from services that allow the obfuscation of viewer identity. These include requests from VPNs, proxies, Tor nodes, and hosting providers (including AWS). This rule group is useful if you want to filter out viewers that might be trying to hide their identity from your application. Blocking the IP addresses of these services can help mitigate bots and evasion of geographic restrictions.

### AWSManagedRulesAmazonIpReputationList

Amazon IP reputation list

VendorName: AWS, Name: AWSManagedRulesAmazonIpReputationList, WCU: 25

The Amazon IP reputation list rule group contains rules that are based on Amazon internal threat intelligence. This is useful if you would like to block IP addresses typically associated with bots or other threats. Blocking these IP addresses can help mitigate bots and reduce the risk of a malicious actor discovering a vulnerable application.

## When You Would Use This Pattern

Anytime you have something exposed to the internet like an API Gateway.

## How To Test This Pattern

After deployment you should see the API Gateway URL in the deployment logs or in the cloudformation output in the console. Take that url and add /prod/helloworld onto the end and open it in a browser - if you see "Hello World!" it worked.

After deployment try changing some of the rules like the geo block one to better understand how it works

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `npm run deploy`      deploy this stack to your default AWS account/region
 * `npm run destroy` destroy all resources from AWS
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
