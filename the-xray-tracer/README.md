# The X-Ray Tracer

This is a pattern not defined by the components used but how they send information back to the AWS X-Ray service to help you make your application closer to Serverless [Well-Architected](https://aws.amazon.com/architecture/well-architected/).

![high level image](img/arch.png)

### The Operational Excellence Pillar

The [operational excellence pillar](https://d1.awsstatic.com/whitepapers/architecture/AWS-Serverless-Applications-Lens.pdf#page=28) includes the ability to run and monitor systems to deliver business value and to continually improve supporting processes and procedures.

> OPS 1: How do you understand the health of your Serverless application?

#### Distributed Tracing
Similar to non-serverless applications, anomalies can occur at larger scale in distributed systems. Due to the nature of serverless architectures, it’s fundamental to have distributed tracing.

Making changes to your serverless application entails many of the same principles of deployment, change, and release management used in traditional workloads. However, there are subtle changes in how you use existing tools to accomplish these principles.

<strong>Active tracing with AWS X-Ray should be enabled to provide distributed tracing capabilities as well as to enable visual service maps for faster troubleshooting</strong>. 

X-Ray helps you identify performance degradation and quickly understand anomalies, including latency distributions.