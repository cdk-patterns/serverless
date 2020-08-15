# The Basic MQ

![architecture](img/the-basic-mq-arch.png)

This is an example cdk stack to deploy [static custom domain endpoints with Amazon MQ](https://aws.amazon.com/blogs/compute/creating-static-custom-domain-endpoints-with-amazon-mq/)  from Rachel Richardson.

In this example we have private Amazon MQ brokers behind an internet-facing network load balancer endpoint using a subdomain.

### Testing broker connectivity

Check "Testing broker connectivity" [here](https://aws.amazon.com/blogs/compute/creating-static-custom-domain-endpoints-with-amazon-mq/).

### Logging into the broker’s ActiveMQ console from a browser

Create a forwarding tunnel through an SSH connection to the bastion host.
First, you need to add a rule allowing SSH connection from your computer, to the security group which the bastion host belongs to (bastionToMQGroup).
You can retrieve bastionToMQGroup's security group ID and add the rule, and below is an example command in the terminal window.

```
SGID=`aws cloudformation describe-stacks --stack-name TheBasicMQStack --region us-east-1 --output json | \
jq -r '.Stacks[0].Outputs[] | select (.OutputKey == "bastionToMQGroupSGID").OutputValue'`
aws ec2 authorize-security-group-ingress --group-id ${SGID} --protocol tcp --port 22 --cidr YOUR-IP-ADDRESS/32
```
Next, push an SSH public key to the bastion host. The key is valid for 60 seconds.

```
InstanceID=`aws cloudformation describe-stacks --stack-name TheBasicMQStack --region us-east-1 --output json | \
jq -r '.Stacks[0].Outputs[] | select (.OutputKey == "bastionInstanceID").OutputValue'`
aws ec2-instance-connect send-ssh-public-key --instance-id ${InstanceID} --instance-os-user ec2-user --ssh-public-key 'file://~/.ssh/id_rsa.pub' --availability-zone us-east-1a
```

Finally, create a forwarding tunnel through an SSH connection to the bastion host.

```
InstancePublicDNS=`aws cloudformation describe-stacks --stack-name TheBasicMQStack --region us-east-1 --output json | \
jq -r '.Stacks[0].Outputs[] | select (.OutputKey == "bastionPublicDNS").OutputValue'`
ssh -D 8162 -N -i ~/.ssh/id_rsa ec2-user@${InstancePublicDNS}
```

Now you are ready to view broker’s ActiveMQ console from a browser. 
Open another window and run `aws mq describe-broker --broker-id myMQ` to get broker's endpoints.
Note only one broker host is active at a time.

If you use Firefox, go to Firefox Connection Settings.  
In the Configure Proxy Access to the Internet section, select Manual proxy configuration, 
then set the SOCKS Host to localhost and Port to 8162, leaving other fields empty.
(See "Creating a forwarding tunnel" [here](https://aws.amazon.com/blogs/compute/creating-static-custom-domain-endpoints-with-amazon-mq/).)

## Available Versions

 * [TypeScript](typescript/)
