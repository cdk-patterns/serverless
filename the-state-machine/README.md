# The State Machine

This is an example CDK stack to deploy The State Machine stack described by Jeremy Daly here - https://www.jeremydaly.com/serverless-microservice-patterns-for-aws/#statemachine

You would use this pattern if you can do your processing asynchronously and you need to have different flows in your logic.

![Architecture](img/the-state-machine-arch.png)

### Stepfunction Logic
![Architecture](img/statemachine.png)


### Testing It Out

After deployment you should have a proxy api gateway where any url hits a lambda which triggers a step function. You can pass in a queryparameter like '?flavour=pepperoni' or '?flavour=pineapple'.

If you pass in pineapple or hawaiian you should see the step function flow fail when you check it via the console.


## Available Versions

 * [TypeScript](typescript/)
 * [Python](python/)
