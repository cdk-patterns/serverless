# The Waf API Gateway

![architecture](img/the-waf-apigateway.png)

This is a cdk stack to deploy a simple API gateway, and attach a WAF ( web applicaiton Firewall ) from Andrew Frazer (<https://github.com/mrpackethead>).

The apigateway stack creates a trival REST apigateway, with a single method which returns 'hello world!' to a GET request. 
THe Waf stack creates a WAF WebACL and attaches it to the the apigateway. It demonstrates a geo-matching rule, and the use of some AWS managed rulesets. This waf stack could be used for any resource that you can attach a WAF rule to ( Such as a load balancer / Cloudfront distribution etc) simply by passing the resources ARN to the stack. 


## Available Versions

 * [TypeScript](typescript/)
 * [Python](python/)

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