import * as cdk from '@aws-cdk/core';
import * as medialive from '@aws-cdk/aws-medialive';
import * as mediapackage from '@aws-cdk/aws-mediapackage';
import * as iam from '@aws-cdk/aws-iam';

const configuration = {
  "id_channel": "test-channel",
  "ip_sg_input": "0.0.0.0/0",
  "stream_name": "test/channel",
  "hls_segment_duration_seconds": 5,
  "hls_playlist_window_seconds": 60,
  "hls_max_video_bits_per_second": 2147483647,
  "hls_min_video_bits_per_second": 0,
  "hls_stream_order": "ORIGINAL"
}

// https://docs.aws.amazon.com/mediaconnect/latest/ug/security_iam_service-with-iam.html
const INLINE_POLICY = {
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogStreams",
      "logs:DescribeLogGroups"
    ],
    "Resource": "arn:aws:logs:*:*:*"
  },
  {
    "Effect": "Allow",
    "Action": [
      "mediaconnect:ManagedDescribeFlow",
      "mediaconnect:ManagedAddOutput",
      "mediaconnect:ManagedRemoveOutput"
    ],
    "Resource": "*"
  },
  {
    "Effect": "Allow",
    "Action": [
      "ec2:describeSubnets",
      "ec2:describeNetworkInterfaces",
      "ec2:createNetworkInterface",
      "ec2:createNetworkInterfacePermission",
      "ec2:deleteNetworkInterface",
      "ec2:deleteNetworkInterfacePermission",
      "ec2:describeSecurityGroups"
    ],
    "Resource": "*"
  },
  {
    "Effect": "Allow",
    "Action": ["mediapackage:DescribeChannel"],
    "Resource": "*"
  }]
}

export class TheMediaLiveStreamStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /*
    * First step: Create MediaPackage Channel
    */
    const channel = new mediapackage.CfnChannel(scope = this,
      id = `media-package-channel-${configuration["id_channel"]}`, {
      id: configuration["id_channel"],
      description: `Channel ${configuration["id_channel"]}`
    });

    /*
    * Second step: Add a HLS endpoint to MediaPackage Channel and output the URL of this endpoint
    */
    const hlsPackage: mediapackage.CfnOriginEndpoint.HlsPackageProperty = {
      segmentDurationSeconds: configuration["hls_segment_duration_seconds"],
      playlistWindowSeconds: configuration["hls_playlist_window_seconds"],
      streamSelection: {
        minVideoBitsPerSecond: configuration["hls_min_video_bits_per_second"],
        maxVideoBitsPerSecond: configuration["hls_max_video_bits_per_second"],
        streamOrder: configuration["hls_stream_order"]
      }
    }

    const hls_endpoint = new mediapackage.CfnOriginEndpoint(scope = this,
      id = `endpoint${configuration["id_channel"]}`, {
      channelId: configuration["id_channel"],
      id: `endpoint${configuration["id_channel"]}`,
      hlsPackage
    });

    // Output the url stream to player
    new cdk.CfnOutput(scope = this, id = "media-package-url-stream", {
      value: hls_endpoint.attrUrl
    });

    /*
    * Third step: Create MediaLive SG, MediaLive Input and MediaLive Channel
    */

    /*
    * Input Security Group
    * Allow 0.0.0.0/0 - Modify it if you want
    */
    const security_groups_input = new medialive.CfnInputSecurityGroup(scope = this,
      id = "media-live-sg-input", {
      whitelistRules: [{ "cidr": configuration["ip_sg_input"] }]
    });

    /*
    * Input with destinations output
    */
    const medialive_input = new medialive.CfnInput(scope = this,
      id = "meddia-input-channel", {
      name: `input- ${configuration["id_channel"]}`,
      type: "RTMP_PUSH",
      inputSecurityGroups: [security_groups_input.ref],
      destinations: [{ streamName: configuration["stream_name"] }]
    });

    /*
    * Media Live Channel Block
    */

    // IAM Role
    let iamRole = new iam.Role(scope = this, id = "medialive_role", {
      roleName: "medialive_role",
      assumedBy: new iam.ServicePrincipal('medialive.amazonaws.com'),
      managedPolicies: [iam.ManagedPolicy.fromAwsManagedPolicyName('AWSElementalMediaLiveFullAccess')],
      inlinePolicies: { "medialivecustom": iam.PolicyDocument.fromJson(INLINE_POLICY) }
    });

    // Channel
    var channelLive = new medialive.CfnChannel(scope = this, id = `media-live-channel-${configuration["id_channel"]}`, {
      channelClass: "SINGLE_PIPELINE",
      name: configuration["id_channel"],
      inputSpecification: {
        codec: "AVC",
        maximumBitrate: "MAX_20_MBPS",
        resolution: "HD"
      },
      inputAttachments: [{
        inputId: medialive_input.ref,
        inputAttachmentName: "attach-input"
      }],
      destinations: [{
        id: "media-destination",
        mediaPackageSettings: [{
          channelId: configuration["id_channel"]
        }]
      }],
      encoderSettings: {
        timecodeConfig: {
          source: "EMBEDDED"
        },
        // Audio descriptions
        audioDescriptions: [{
          audioSelectorName: "Default",
          audioTypeControl: "FOLLOW_INPUT",
          languageCodeControl: "FOLLOW_INPUT",
          name: "audio_1",
          codecSettings: {
            aacSettings: {
              bitrate: 192000,
              codingMode: "CODING_MODE_2_0",
              inputType: "NORMAL",
              profile: "LC",
              rateControlMode: "CBR",
              rawFormat: "NONE",
              sampleRate: 48000,
              spec: "MPEG4"
            }
          }
        },
        {
          audioSelectorName: "Default",
          audioTypeControl: "FOLLOW_INPUT",
          languageCodeControl: "FOLLOW_INPUT",
          name: "audio_2",
          codecSettings: {
            aacSettings: {
              bitrate: 192000,
              codingMode: "CODING_MODE_2_0",
              inputType: "NORMAL",
              profile: "LC",
              rateControlMode: "CBR",
              rawFormat: "NONE",
              sampleRate: 48000,
              spec: "MPEG4"
            }
          }
        }],
        // Video descriptions
        videoDescriptions: [{
          codecSettings: {
            h264Settings: {
              adaptiveQuantization: "HIGH",
              afdSignaling: "NONE",
              bitrate: 5000000,
              colorMetadata: "INSERT",
              entropyEncoding: "CABAC",
              flickerAq: "ENABLED",
              framerateControl: "SPECIFIED",
              framerateDenominator: 1,
              framerateNumerator: 50,
              gopBReference: "ENABLED",
              gopClosedCadence: 1,
              gopNumBFrames: 3,
              gopSize: 60,
              gopSizeUnits: "FRAMES",
              level: "H264_LEVEL_AUTO",
              lookAheadRateControl: "HIGH",
              numRefFrames: 3,
              parControl: "SPECIFIED",
              profile: "HIGH",
              rateControlMode: "CBR",
              scanType: "PROGRESSIVE",
              sceneChangeDetect: "ENABLED",
              slices: 1,
              spatialAq: "ENABLED",
              syntax: "DEFAULT",
              temporalAq: "ENABLED",
              timecodeInsertion: "DISABLED"
            }
          },
          height: 1080,
          name: "video_1080p30",
          respondToAfd: "NONE",
          scalingBehavior: "DEFAULT",
          sharpness: 50,
          width: 1920
        },
        {
          codecSettings: {
            h264Settings: {
              adaptiveQuantization: "HIGH",
              afdSignaling: "NONE",
              bitrate: 3000000,
              colorMetadata: "INSERT",
              entropyEncoding: "CABAC",
              flickerAq: "ENABLED",
              framerateControl: "SPECIFIED",
              framerateDenominator: 1,
              framerateNumerator: 50,
              gopBReference: "ENABLED",
              gopClosedCadence: 1,
              gopNumBFrames: 3,
              gopSize: 60,
              gopSizeUnits: "FRAMES",
              level: "H264_LEVEL_AUTO",
              lookAheadRateControl: "HIGH",
              numRefFrames: 3,
              parControl: "SPECIFIED",
              profile: "HIGH",
              rateControlMode: "CBR",
              scanType: "PROGRESSIVE",
              sceneChangeDetect: "ENABLED",
              slices: 1,
              spatialAq: "ENABLED",
              syntax: "DEFAULT",
              temporalAq: "ENABLED",
              timecodeInsertion: "DISABLED"
            }
          },
          height: 720,
          name: "video_720p30",
          respondToAfd: "NONE",
          scalingBehavior: "DEFAULT",
          sharpness: 100,
          width: 1280
        }
        ],
        // Output groups
        outputGroups: [{
          name: "HD",
          outputGroupSettings: {
            mediaPackageGroupSettings: {
              destination: {
                destinationRefId: "media-destination"
              }
            }
          },
          outputs: [{
            audioDescriptionNames: ["audio_1"],
            outputName: "1080p30",
            videoDescriptionName: "video_1080p30",
            outputSettings: {
              mediaPackageOutputSettings: {}
            }
          },
          {
            audioDescriptionNames: ["audio_2"],
            outputName: "720p30",
            videoDescriptionName: "video_720p30",
            outputSettings: {
              mediaPackageOutputSettings: {}
            }
          }]
        }]
      },
      roleArn: iamRole.roleArn
    });

    // We need to add dependency because CFN must wait channel creation finish before starting the endpoint creation  
    var mediadep = new cdk.ConcreteDependable();
    mediadep.add(channel);
    hls_endpoint.node.addDependency(mediadep);
    channelLive.node.addDependency(mediadep);

  }

}
