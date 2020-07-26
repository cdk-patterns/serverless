"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const { ECS } = require('aws-sdk');
const AWS = require('aws-sdk');
AWS.config.region = process.env.AWS_REGION || 'us-east-1';
const eventbridge = new AWS.EventBridge();
exports.handler = async function (event) {
    var _a, _b, _c, _d, _e, _f, _g, _h, _j;
    var ecs = new ECS({ apiVersion: '2014-11-13' });
    console.log("request:", JSON.stringify(event, undefined, 2));
    let records = event.Records;
    //Exract variables from environment
    const clusterName = process.env.CLUSTER_NAME;
    if (typeof clusterName == 'undefined') {
        throw new Error('Cluster Name is not defined');
    }
    const taskDefinition = process.env.TASK_DEFINITION;
    if (typeof taskDefinition == 'undefined') {
        throw new Error('Task Definition is not defined');
    }
    const subNets = process.env.SUBNETS;
    if (typeof subNets == 'undefined') {
        throw new Error('SubNets are not defined');
    }
    const containerName = process.env.CONTAINER_NAME;
    if (typeof containerName == 'undefined') {
        throw new Error('Container Name is not defined');
    }
    console.log('Cluster Name - ' + clusterName);
    console.log('Task Definition - ' + taskDefinition);
    console.log('SubNets - ' + subNets);
    var params = {
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
        console.log('records ' + s3eventRecords);
        for (let i in s3eventRecords) {
            let s3event = s3eventRecords[i];
            console.log('s3 event ' + s3event);
            //Extract variables from event
            const objectKey = (_c = (_b = (_a = s3event) === null || _a === void 0 ? void 0 : _a.s3) === null || _b === void 0 ? void 0 : _b.object) === null || _c === void 0 ? void 0 : _c.key;
            const bucketName = (_f = (_e = (_d = s3event) === null || _d === void 0 ? void 0 : _d.s3) === null || _e === void 0 ? void 0 : _e.bucket) === null || _f === void 0 ? void 0 : _f.name;
            const bucketARN = (_j = (_h = (_g = s3event) === null || _g === void 0 ? void 0 : _g.s3) === null || _h === void 0 ? void 0 : _h.bucket) === null || _j === void 0 ? void 0 : _j.arn;
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
                };
                let ecsResponse = await ecs.runTask(params).promise().catch((error) => {
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
                const result = await eventbridge.putEvents(eventBridgeParams).promise().catch((error) => {
                    throw new Error(error);
                });
                console.log(result);
            }
            else {
                console.log('not an s3 event...');
            }
        }
    }
};
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiczNTcXNFdmVudENvbnN1bWVyLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiczNTcXNFdmVudENvbnN1bWVyLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7O0FBQUEsTUFBTSxFQUFFLEdBQUcsRUFBRSxHQUFHLE9BQU8sQ0FBQyxTQUFTLENBQUMsQ0FBQztBQUNuQyxNQUFNLEdBQUcsR0FBRyxPQUFPLENBQUMsU0FBUyxDQUFDLENBQUM7QUFFL0IsR0FBRyxDQUFDLE1BQU0sQ0FBQyxNQUFNLEdBQUcsT0FBTyxDQUFDLEdBQUcsQ0FBQyxVQUFVLElBQUksV0FBVyxDQUFBO0FBQ3pELE1BQU0sV0FBVyxHQUFHLElBQUksR0FBRyxDQUFDLFdBQVcsRUFBRSxDQUFBO0FBRXpDLE9BQU8sQ0FBQyxPQUFPLEdBQUcsS0FBSyxXQUFXLEtBQVU7O0lBQ3hDLElBQUksR0FBRyxHQUFHLElBQUksR0FBRyxDQUFDLEVBQUUsVUFBVSxFQUFFLFlBQVksRUFBRSxDQUFDLENBQUM7SUFFaEQsT0FBTyxDQUFDLEdBQUcsQ0FBQyxVQUFVLEVBQUUsSUFBSSxDQUFDLFNBQVMsQ0FBQyxLQUFLLEVBQUUsU0FBUyxFQUFFLENBQUMsQ0FBQyxDQUFDLENBQUM7SUFDN0QsSUFBSSxPQUFPLEdBQVUsS0FBSyxDQUFDLE9BQU8sQ0FBQztJQUVuQyxtQ0FBbUM7SUFDbkMsTUFBTSxXQUFXLEdBQUcsT0FBTyxDQUFDLEdBQUcsQ0FBQyxZQUFZLENBQUM7SUFDN0MsSUFBSSxPQUFPLFdBQVcsSUFBSSxXQUFXLEVBQUU7UUFDbkMsTUFBTSxJQUFJLEtBQUssQ0FBQyw2QkFBNkIsQ0FBQyxDQUFBO0tBQ2pEO0lBRUQsTUFBTSxjQUFjLEdBQUcsT0FBTyxDQUFDLEdBQUcsQ0FBQyxlQUFlLENBQUM7SUFDbkQsSUFBSSxPQUFPLGNBQWMsSUFBSSxXQUFXLEVBQUU7UUFDdEMsTUFBTSxJQUFJLEtBQUssQ0FBQyxnQ0FBZ0MsQ0FBQyxDQUFBO0tBQ3BEO0lBRUQsTUFBTSxPQUFPLEdB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O2lCQUNKLENBQUE7Z0JBRUQsSUFBSSxXQUFXLEdBQUcsTUFBTSxHQUFHLENBQUMsT0FBTyxDQUFDLE1BQU0sQ0FBQyxDQUFDLE9BQU8sRUFBRSxDQUFDLEtBQUssQ0FBQyxDQUFDLEtBQVUsRUFBRSxFQUFFO29CQUN2RSxNQUFNLElBQUksS0FBSyxDQUFDLEtBQUssQ0FBQyxDQUFDO2dCQUMzQixDQUFDLENBQUMsQ0FBQztnQkFFSCxPQUFPLENBQUMsR0FBRyxDQUFDLFdBQVcsQ0FBQyxDQUFDO2dCQUV4QixpREFBaUQ7Z0JBQ2xELElBQUksaUJBQWlCLEdBQUc7b0JBQ3BCLE9BQU8sRUFBRTt3QkFDVDs0QkFDSSxVQUFVLEVBQUUsYUFBYTs0QkFDekIsWUFBWSxFQUFFLFNBQVM7NEJBQ3ZCLE1BQU0sRUFBRSxpQ0FBaUM7NEJBQ3pDLElBQUksRUFBRSxJQUFJLElBQUksRUFBRTs0QkFDaEIsa0JBQWtCOzRCQUNsQixNQUFNLEVBQUUsSUFBSSxDQUFDLFNBQVMsQ0FBQztnQ0FDbkIsTUFBTSxFQUFFLFNBQVM7Z0NBQ2pCLElBQUksRUFBRSxXQUFXOzZCQUNwQixDQUFDO3lCQUNMO3FCQUNBO2lCQUNKLENBQUM7Z0JBRUYsTUFBTSxNQUFNLEdBQUcsTUFBTSxXQUFXLENBQUMsU0FBUyxDQUFDLGlCQUFpQixDQUFDLENBQUMsT0FBTyxFQUFFLENBQUMsS0FBSyxDQUFDLENBQUMsS0FBVSxFQUFFLEVBQUU7b0JBQ3pGLE1BQU0sSUFBSSxLQUFLLENBQUMsS0FBSyxDQUFDLENBQUM7Z0JBQzNCLENBQUMsQ0FBQyxDQUFDO2dCQUNILE9BQU8sQ0FBQyxHQUFHLENBQUMsTUFBTSxDQUFDLENBQUM7YUFDdkI7aUJBQU07Z0JBQ0gsT0FBTyxDQUFDLEdBQUcsQ0FBQyxvQkFBb0IsQ0FBQyxDQUFBO2FBQ3BDO1NBQ0o7S0FDSjtBQUNMLENBQUMsQ0FBQyIsInNvdXJjZXNDb250ZW50IjpbImNvbnN0IHsgRUNTIH0gPSByZXF1aXJlKCdhd3Mtc2RrJyk7XG5jb25zdCBBV1MgPSByZXF1aXJlKCdhd3Mtc2RrJyk7XG5leHBvcnQge307XG5BV1MuY29uZmlnLnJlZ2lvbiA9IHByb2Nlc3MuZW52LkFXU19SRUdJT04gfHwgJ3VzLWVhc3QtMSdcbmNvbnN0IGV2ZW50YnJpZGdlID0gbmV3IEFXUy5FdmVudEJyaWRnZSgpXG5cbmV4cG9ydHMuaGFuZGxlciA9IGFzeW5jIGZ1bmN0aW9uIChldmVudDogYW55KSB7XG4gICAgdmFyIGVjcyA9IG5ldyBFQ1MoeyBhcGlWZXJzaW9uOiAnMjAxNC0xMS0xMycgfSk7XG5cbiAgICBjb25zb2xlLmxvZyhcInJlcXVlc3Q6XCIsIEpTT04uc3RyaW5naWZ5KGV2ZW50LCB1bmRlZmluZWQsIDIpKTtcbiAgICBsZXQgcmVjb3JkczogYW55W10gPSBldmVudC5SZWNvcmRzO1xuXG4gICAgLy9FeHJhY3QgdmFyaWFibGVzIGZyb20gZW52aXJvbm1lbnRcbiAgICBjb25zdCBjbHVzdGVyTmFtZSA9IHByb2Nlc3MuZW52LkNMVVNURVJfTkFNRTtcbiAgICBpZiAodHlwZW9mIGNsdXN0ZXJOYW1lID09ICd1bmRlZmluZWQnKSB7XG4gICAgICAgIHRocm93IG5ldyBFcnJvcignQ2x1c3RlciBOYW1lIGlzIG5vdCBkZWZpbmVkJylcbiAgICB9XG5cbiAgICBjb25zdCB0YXNrRGVmaW5pdGlvbiA9IHByb2Nlc3MuZW52LlRBU0tfREVGSU5JVElPTjtcbiAgICBpZiAodHlwZW9mIHRhc2tEZWZpbml0aW9uID09ICd1bmRlZmluZWQnKSB7XG4gICAgICAgIHRocm93IG5ldyBFcnJvcignVGFzayBEZWZpbml0aW9uIGlzIG5vdCBkZWZpbmVkJylcbiAgICB9XG5cbiAgICBjb25zdCBzdWJOZXRzID0gcHJvY2Vzcy5lbnYuU1VCTkVUUztcbiAgICBpZiAodHlwZW9mIHN1Yk5ldHMgPT0gJ3VuZGVmaW5lZCcpIHtcbiAgICAgICAgdGhyb3cgbmV3IEVycm9yKCdTdWJOZXRzIGFyZSBub3QgZGVmaW5lZCcpXG4gICAgfVxuXG4gICAgY29uc3QgY29udGFpbmVyTmFtZSA9IHByb2Nlc3MuZW52LkNPTlRBSU5FUl9OQU1FO1xuICAgIGlmICh0eXBlb2YgY29udGFpbmVyTmFtZSA9PSAndW5kZWZpbmVkJykge1xuICAgICAgICB0aHJvdyBuZXcgRXJyb3IoJ0NvbnRhaW5lciBOYW1lIGlzIG5vdCBkZWZpbmVkJylcbiAgICB9XG5cbiAgICBjb25zb2xlLmxvZygnQ2x1c3RlciBOYW1lIC0gJyArIGNsdXN0ZXJOYW1lKTtcbiAgICBjb25zb2xlLmxvZygnVGFzayBEZWZpbml0aW9uIC0gJyArIHRhc2tEZWZpbml0aW9uKTtcbiAgICBjb25zb2xlLmxvZygnU3ViTmV0cyAtICcgKyBzdWJOZXRzKTtcblxuICAgIHZhciBwYXJhbXM6YW55ID0ge1xuICAgICAgICBjbHVzdGVyOiBjbHVzdGVyTmFtZSxcbiAgICAgICAgbGF1bmNoVHlwZTogJ0ZBUkdBVEUnLFxuICAgICAgICB0YXNrRGVmaW5pdGlvbjogdGFza0RlZmluaXRpb24sXG4gICAgICAgIGNvdW50OiAxLFxuICAgICAgICBwbGF0Zm9ybVZlcnNpb246ICdMQVRFU1QnLFxuICAgICAgICBuZXR3b3JrQ29uZmlndXJhdGlvbjoge1xuICAgICAgICAgICAgJ2F3c3ZwY0NvbmZpZ3VyYXRpb24nOiB7XG4gICAgICAgICAgICAgICAgJ3N1Ym5ldHMnOiBKU09OLnBhcnNlKHN1Yk5ldHMpLFxuICAgICAgICAgICAgICAgICdhc3NpZ25QdWJsaWNJcCc6ICdESVNBQkxFRCdcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH07XG5cbiAgICAvKipcbiAgICAgKiBBbiBldmVudCBjYW4gY29udGFpbiBtdWx0aXBsZSByZWNvcmRzIHRvIHByb2Nlc3MuIGkuZS4gdGhlIHVzZXIgY291bGQgaGF2ZSB1cGxvYWRlZCAyIGZpbGVzLlxuICAgICAqL1xuICAgIGZvciAobGV0IGluZGV4IGluIHJlY29yZHMpIHtcbiAgICAgICAgbGV0IHBheWxvYWQgPSBKU09OLnBhcnNlKHJlY29yZHNbaW5kZXhdLmJvZHkpO1xuICAgICAgICBjb25zb2xlLmxvZygncHJvY2Vzc2luZyBzMyBldmVudHMgJyArIHBheWxvYWQpO1xuXG4gICAgICAgIGxldCBzM2V2ZW50UmVjb3JkcyA9IHBheWxvYWQuUmVjb3JkcztcblxuICAgICAgICBjb25zb2xlLmxvZygncmVjb3JkcyAnKyBzM2V2ZW50UmVjb3Jkcyk7XG5cbiAgICAgICAgZm9yIChsZXQgaSBpbiBzM2V2ZW50UmVjb3Jkcykge1xuXG4gICAgICAgICAgICBsZXQgczNldmVudCA9ICBzM2V2ZW50UmVjb3Jkc1tpXTtcbiAgICAgICAgICAgIGNvbnNvbGUubG9nKCdzMyBldmVudCAnKyBzM2V2ZW50KVxuXG4gICAgICAgICAgICAvL0V4dHJhY3QgdmFyaWFibGVzIGZyb20gZXZlbnRcbiAgICAgICAgICAgIGNvbnN0IG9iamVjdEtleSA9IHMzZXZlbnQ/LnMzPy5vYmplY3Q/LmtleTtcbiAgICAgICAgICAgIGNvbnN0IGJ1Y2tldE5hbWUgPSBzM2V2ZW50Py5zMz8uYnVja2V0Py5uYW1lO1xuICAgICAgICAgICAgY29uc3QgYnVja2V0QVJOID0gczNldmVudD8uczM/LmJ1Y2tldD8uYXJuO1xuXG4gICAgICAgICAgICBjb25zb2xlLmxvZygnT2JqZWN0IEtleSAtICcgKyBvYmplY3RLZXkpO1xuICAgICAgICAgICAgY29uc29sZS5sb2coJ0J1Y2tldCBOYW1lIC0gJyArIGJ1Y2tldE5hbWUpO1xuICAgICAgICAgICAgY29uc29sZS5sb2coJ0J1Y2tldCBBUk4gLSAnICsgYnVja2V0QVJOKTtcblxuICAgICAgICAgICAgaWYgKCh0eXBlb2YgKG9iamVjdEtleSkgIT0gJ3VuZGVmaW5lZCcpICYmXG4gICAgICAgICAgICAgICAgKHR5cGVvZiAoYnVja2V0TmFtZSkgIT0gJ3VuZGVmaW5lZCcpICYmXG4gICAgICAgICAgICAgICAgKHR5cGVvZiAoYnVja2V0QVJOKSAhPSAndW5kZWZpbmVkJykpIHtcblxuICAgICAgICAgICAgICAgIHBhcmFtcy5vdmVycmlkZXMgPSB7XG4gICAgICAgICAgICAgICAgICAgIGNvbnRhaW5lck92ZXJyaWRlczogW1xuICAgICAgICAgICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGVudmlyb25tZW50OiBbXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU6ICdTM19CVUNLRVRfTkFNRScsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZTogYnVja2V0TmFtZVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBuYW1lOiAnUzNfT0JKRUNUX0tFWScsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZTogb2JqZWN0S2V5XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBdLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU6IGNvbnRhaW5lck5hbWVcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgXVxuICAgICAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgICAgIGxldCBlY3NSZXNwb25zZSA9IGF3YWl0IGVjcy5ydW5UYXNrKHBhcmFtcykucHJvbWlzZSgpLmNhdGNoKChlcnJvcjogYW55KSA9PiB7XG4gICAgICAgICAgICAgICAgICAgIHRocm93IG5ldyBFcnJvcihlcnJvcik7XG4gICAgICAgICAgICAgICAgfSk7XG5cbiAgICAgICAgICAgICAgICBjb25zb2xlLmxvZyhlY3NSZXNwb25zZSk7XG5cbiAgICAgICAgICAgICAgICAgLy8gQnVpbGRpbmcgb3VyIGVjcyBzdGFydGVkIGV2ZW50IGZvciBFdmVudEJyaWRnZVxuICAgICAgICAgICAgICAgIHZhciBldmVudEJyaWRnZVBhcmFtcyA9IHtcbiAgICAgICAgICAgICAgICAgICAgRW50cmllczogW1xuICAgICAgICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgICAgICAgICBEZXRhaWxUeXBlOiAnZWNzLXN0YXJ0ZWQnLFxuICAgICAgICAgICAgICAgICAgICAgICAgRXZlbnRCdXNOYW1lOiAnZGVmYXVsdCcsXG4gICAgICAgICAgICAgICAgICAgICAgICBTb3VyY2U6ICdjZGtwYXR0ZXJucy50aGUtZXZlbnRicmlkZ2UtZXRsJyxcbiAgICAgICAgICAgICAgICAgICAgICAgIFRpbWU6IG5ldyBEYXRlKCksXG4gICAgICAgICAgICAgICAgICAgICAgICAvLyBNYWluIGV2ZW50IGJvZHlcbiAgICAgICAgICAgICAgICAgICAgICAgIERldGFpbDogSlNPTi5zdHJpbmdpZnkoe1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHN0YXR1czogJ3N1Y2Nlc3MnLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRhdGE6IGVjc1Jlc3BvbnNlXG4gICAgICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIF1cbiAgICAgICAgICAgICAgICB9O1xuICAgICAgICAgICAgICAgIFxuICAgICAgICAgICAgICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IGV2ZW50YnJpZGdlLnB1dEV2ZW50cyhldmVudEJyaWRnZVBhcmFtcykucHJvbWlzZSgpLmNhdGNoKChlcnJvcjogYW55KSA9PiB7XG4gICAgICAgICAgICAgICAgICAgIHRocm93IG5ldyBFcnJvcihlcnJvcik7XG4gICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgY29uc29sZS5sb2cocmVzdWx0KTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgY29uc29sZS5sb2coJ25vdCBhbiBzMyBldmVudC4uLicpXG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICB9XG59OyJdfQ==