const { ECS } = require('aws-sdk');
const AWS = require('aws-sdk');
export {};
AWS.config.region = process.env.AWS_REGION || 'us-east-1'
const eventbridge = new AWS.EventBridge()

exports.handler = async function (event: any) {
    var ecs = new ECS({ apiVersion: '2014-11-13' });

    console.log("request:", JSON.stringify(event, undefined, 2));
    let records: any[] = event.Records;

    //Exract variables from environment
    const clusterName = process.env.CLUSTER_NAME;
    if (typeof clusterName == 'undefined') {
        throw new Error('Cluster Name is not defined')
    }

    const taskDefinition = process.env.TASK_DEFINITION;
    if (typeof taskDefinition == 'undefined') {
        throw new Error('Task Definition is not defined')
    }

    const subNets = process.env.SUBNETS;
    if (typeof subNets == 'undefined') {
        throw new Error('SubNets are not defined')
    }

    const containerName = process.env.CONTAINER_NAME;
    if (typeof containerName == 'undefined') {
        throw new Error('Container Name is not defined')
    }

    console.log('Cluster Name - ' + clusterName);
    console.log('Task Definition - ' + taskDefinition);
    console.log('SubNets - ' + subNets);

    var params:any = {
        cluster: clusterName,
        launchType: 'FARGATE',
        taskDefinition: taskDefinition,
        count: 1,
        platformVersion: 'LATEST',
        networkConfiguration: {
            'awsvpcConfiguration': {
                'subnets': JSON.parse(subNets),
                'assignPublicIp': 'DISABLED'
            }
        }
    };

    /**
     * An event can contain multiple records to process. i.e. the user could have uploaded 2 files.
     */
    for (let index in records) {
        let payload = JSON.parse(records[index].body);
        console.log('processing s3 events ' + payload);

        let s3eventRecords = payload.Records;

        console.log('records '+ s3eventRecords);

        for (let i in s3eventRecords) {

            let s3event =  s3eventRecords[i];
            console.log('s3 event '+ s3event)

            //Extract variables from event
            const objectKey = s3event?.s3?.object?.key;
            const bucketName = s3event?.s3?.bucket?.name;
            const bucketARN = s3event?.s3?.bucket?.arn;

            console.log('Object Key - ' + objectKey);
            console.log('Bucket Name - ' + bucketName);
            console.log('Bucket ARN - ' + bucketARN);

            if ((typeof (objectKey) != 'undefined') &&
                (typeof (bucketName) != 'undefined') &&
                (typeof (bucketARN) != 'undefined')) {

                params.overrides = {
                    containerOverrides: [
                        {
                            environment: [
                                {
                                    name: 'S3_BUCKET_NAME',
                                    value: bucketName
                                },
                                {
                                    name: 'S3_OBJECT_KEY',
                                    value: objectKey
                                }
                            ],
                            name: containerName
                        }
                    ]
                }

                let ecsResponse = await ecs.runTask(params).promise().catch((error: any) => {
                    throw new Error(error);
                });

                console.log(ecsResponse);

                 // Building our ecs started event for EventBridge
                var eventBridgeParams = {
                    Entries: [
                    {
                        DetailType: 'ecs-started',
                        EventBusName: 'default',
                        Source: 'cdkpatterns.the-eventbridge-etl',
                        Time: new Date(),
                        // Main event body
                        Detail: JSON.stringify({
                            status: 'success',
                            data: ecsResponse
                        })
                    }
                    ]
                };
                
                const result = await eventbridge.putEvents(eventBridgeParams).promise().catch((error: any) => {
                    throw new Error(error);
                });
                console.log(result);
            } else {
                console.log('not an s3 event...')
            }
        }
    }
};