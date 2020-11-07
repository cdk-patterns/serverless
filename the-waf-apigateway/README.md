# The Waf API Gateway


This is a cdk stack to deploy a simple API gateway, and attach a WAF ( web applicaiton Firewall ) from Andrew Frazer ( <https://github.com/mrpackethead> ) .

![architecture](img/the-waf-apigateway.png)

This stack implements three stacks,  A 'Top' level stack from where 'component' stacks are nested.  This approach logically seperates resources together, allowing better code reuse, and overall understanding. 

The apigateway stack creates a trival REST apigateway, with a single method which returns 'hello-world' to a POST request. 
THe Waf stack creates a WAF WebACL and attaches it to the the apigateway.    It demonstrates a geo-matching rule, and the use of some AWS managed rulesets.    This waf stack could be used for any resource that you can attach a WAF rule to ( Such as a load balancer / Cloudfront distribution etc) simply by passing the resources ARN to the stack. 


## Available Versions

 * [Python](python/)

