# The Waf API Gateway



This is an example cdk stack to deploy "The WAF API Gateway" from Andrew Frazer. It demonstrates creating an API gateway, and a WAF ACL, and attaching the WAF ACL to the API Gateway.  

In this example we have an API Gateway with a "/helloworld" endpoint that takes a GET request.  The WAF ACL is configured to block traffic that does not match the list of countrys, and also check that the sender is not on AWS's lists of Bad actors. 



## Available Versions

 * [Python](python/)

