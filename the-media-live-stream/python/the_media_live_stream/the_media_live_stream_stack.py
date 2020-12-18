from aws_cdk import (
    core, aws_medialive as medialive, aws_iam as iam, aws_mediapackage as mediapackage
)

DEFAULT_CONF = {
    "id_channel": "test-channel",
    "ip_sg_input": "0.0.0.0/0",
    "stream_name": "test/channel",
    "hls_segment_duration_seconds": 5,
    "hls_playlist_window_seconds": 60,
    "hls_max_video_bits_per_second": 2147483647,
    "hls_min_video_bits_per_second": 0,
    "hls_stream_order": "ORIGINAL"
}

# https://docs.aws.amazon.com/mediaconnect/latest/ug/security_iam_service-with-iam.html
INLINE_POLICY = {"Version": "2012-10-17",
                 "Statement": [{"Effect": "Allow",
                                "Action": ["logs:CreateLogGroup", "logs:CreateLogStream",
                                           "logs:PutLogEvents", "logs:DescribeLogStreams",
                                           "logs:DescribeLogGroups"],
                                "Resource": "arn:aws:logs:*:*:*"},
                               {"Effect": "Allow",
                                "Action": [
                                    "mediaconnect:ManagedDescribeFlow",
                                    "mediaconnect:ManagedAddOutput",
                                    "mediaconnect:ManagedRemoveOutput"],
                                "Resource": "*"},
                               {"Effect": "Allow",
                                "Action": ["ec2:describeSubnets",
                                           "ec2:describeNetworkInterfaces",
                                           "ec2:createNetworkInterface",
                                           "ec2:createNetworkInterfacePermission",
                                           "ec2:deleteNetworkInterface",
                                           "ec2:deleteNetworkInterfacePermission",
                                           "ec2:describeSecurityGroups"],
                                "Resource": "*"},
                               {"Effect": "Allow",
                                "Action": ["mediapackage:DescribeChannel"],
                                "Resource": "*"
                                }]
                 }


class TheMediaLiveStreamStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """
        First step: Create MediaPackage Channel
        """
        channel = mediapackage.CfnChannel(scope=self,
                                          id_="media-package-channel-{0}".format(DEFAULT_CONF.get("id_channel")),
                                          id=DEFAULT_CONF.get("id_channel"),
                                          description="Channel {0}".format(DEFAULT_CONF.get("id_channel")))

        """
        Second step: Add a HLS endpoint to MediaPackage Channel and output the URL of this endpoint
        """
        hsl_endpoint_package = mediapackage.CfnOriginEndpoint.HlsPackageProperty(
            segment_duration_seconds=DEFAULT_CONF.get("hls_segment_duration_seconds"),
            playlist_window_seconds=DEFAULT_CONF.get("hls_playlist_window_seconds"),
            stream_selection=mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                max_video_bits_per_second=DEFAULT_CONF.get("hls_max_video_bits_per_second"),
                min_video_bits_per_second=DEFAULT_CONF.get("hls_min_video_bits_per_second"),
                stream_order=DEFAULT_CONF.get("hls_stream_order")
            ))

        hls_endpoint = mediapackage.CfnOriginEndpoint(scope=self,
                                                      id_="endpoint-{0}".format(DEFAULT_CONF.get("id_channel")),
                                                      id=DEFAULT_CONF.get("id_channel"),
                                                      channel_id=format(DEFAULT_CONF.get("id_channel")),
                                                      description="Endpoint - {0}".format(
                                                          DEFAULT_CONF.get("id_channel")),
                                                      hls_package=hsl_endpoint_package)

        # Output the url stream to player
        core.CfnOutput(scope=self, id="media-package-url-stream", value=hls_endpoint.attr_url)

        """
        Third step: Create MediaLive SG, MediaLive Input and MediaLive Channel
        """
        """ 
        Input Security Group
        Allow 0.0.0.0/0 - Modify it if you want """
        security_groups_input = medialive.CfnInputSecurityGroup(scope=self,
                                                                id="media-live-sg-input",
                                                                whitelist_rules=[
                                                                    {"cidr": DEFAULT_CONF.get("ip_sg_input")}])

        """ Input destination """
        media_live_input_destination = medialive.CfnInput.InputDestinationRequestProperty(
            stream_name=DEFAULT_CONF.get("stream_name"))

        """ Input with destinations output """
        medialive_input = medialive.CfnInput(scope=self,
                                             id="media-input-channel",
                                             name="input-test1",
                                             type="RTMP_PUSH",
                                             input_security_groups=[security_groups_input.ref],
                                             destinations=[media_live_input_destination])

        """ Media Live Channel Block """
        media_live_channel_input_spec = medialive.CfnChannel.InputSpecificationProperty(codec="AVC",
                                                                                        maximum_bitrate="MAX_20_MBPS",
                                                                                        resolution="HD")

        media_live_channel_input_attach = medialive.CfnChannel.InputAttachmentProperty(input_id=medialive_input.ref,
                                                                                       input_attachment_name="attach-input-test1")

        media_live_channel_destination_settings = medialive.CfnChannel.MediaPackageOutputDestinationSettingsProperty(
            channel_id=DEFAULT_CONF.get("id_channel"))
        media_live_channel_destination = medialive.CfnChannel.OutputDestinationProperty(id="media-destination",
                                                                                        media_package_settings=[
                                                                                            media_live_channel_destination_settings])

        """
        We need to control bitrate based on user connection. The manifest will include 2 video quality:
        video_720p30 = bitrate 3000000
        video_1080p30 = bitrate 5000000
        Let's go create them
        You can create more resolutions based on bitrate, like:
        video_240p30 = bitrate 750000
        video_480p30 = bitrate 1500000
        """
        # Audio + output + video

        """ Audio Section """
        audio_aac = medialive.CfnChannel.AacSettingsProperty(bitrate=192000, coding_mode="CODING_MODE_2_0",
                                                             input_type="NORMAL",
                                                             profile="LC", rate_control_mode="CBR", raw_format="NONE",
                                                             sample_rate=48000, spec="MPEG4")
        audio_codec = medialive.CfnChannel.AudioCodecSettingsProperty(aac_settings=audio_aac)
        audio1 = medialive.CfnChannel.AudioDescriptionProperty(audio_selector_name="Default",
                                                               audio_type_control="FOLLOW_INPUT",
                                                               language_code_control="FOLLOW_INPUT",
                                                               name="audio_1",
                                                               codec_settings=audio_codec)
        audio2 = medialive.CfnChannel.AudioDescriptionProperty(audio_selector_name="Default",
                                                               audio_type_control="FOLLOW_INPUT",
                                                               language_code_control="FOLLOW_INPUT",
                                                               name="audio_2",
                                                               codec_settings=audio_codec)

        """ Output Section """
        output_mediapackage_destination_ref = medialive.CfnChannel.OutputLocationRefProperty(destination_ref_id="media-destination")
        output_mediapackage_destination = medialive.CfnChannel.MediaPackageGroupSettingsProperty(destination=output_mediapackage_destination_ref)
        output_settings = medialive.CfnChannel.OutputGroupSettingsProperty(media_package_group_settings=output_mediapackage_destination)

        output_output1 = medialive.CfnChannel.OutputProperty(audio_description_names=["audio_1"],
                                                             output_name="1080p30",
                                                             video_description_name="video_1080p30",
                                                             output_settings=medialive.CfnChannel.OutputSettingsProperty(
                                                                 media_package_output_settings={}
                                                             ))

        output_output2 = medialive.CfnChannel.OutputProperty(audio_description_names=["audio_2"],
                                                             output_name="720p30",
                                                             video_description_name="video_720p30",
                                                             output_settings=medialive.CfnChannel.OutputSettingsProperty(
                                                                 media_package_output_settings={}
                                                             ))

        output = medialive.CfnChannel.OutputGroupProperty(name="HD", output_group_settings=output_settings,
                                                          outputs=[output_output1, output_output2])

        """ Video Section """
        video1_h264 = medialive.CfnChannel.H264SettingsProperty(adaptive_quantization="HIGH", afd_signaling="NONE",
                                                                bitrate=5000000, color_metadata="INSERT",
                                                                entropy_encoding="CABAC",
                                                                flicker_aq="ENABLED", framerate_control="SPECIFIED",
                                                                framerate_denominator=1, framerate_numerator=30,
                                                                gop_b_reference="ENABLED",
                                                                gop_closed_cadence=1, gop_num_b_frames=3, gop_size=60,
                                                                gop_size_units="FRAMES",
                                                                level="H264_LEVEL_AUTO", look_ahead_rate_control="HIGH",
                                                                num_ref_frames=3,
                                                                par_control="SPECIFIED", profile="HIGH",
                                                                rate_control_mode="CBR",
                                                                scan_type="PROGRESSIVE", scene_change_detect="ENABLED",
                                                                slices=1,
                                                                spatial_aq="ENABLED", syntax="DEFAULT",
                                                                temporal_aq="ENABLED",
                                                                timecode_insertion="DISABLED")
        video1_codec = medialive.CfnChannel.VideoCodecSettingsProperty(h264_settings=video1_h264)
        video1_description = medialive.CfnChannel.VideoDescriptionProperty(codec_settings=video1_codec, height=1080,
                                                                           name="video_1080p30", respond_to_afd="NONE",
                                                                           scaling_behavior="DEFAULT", sharpness=50,
                                                                           width=1920)

        video2_h264 = medialive.CfnChannel.H264SettingsProperty(adaptive_quantization="HIGH", afd_signaling="NONE",
                                                                bitrate=3000000, color_metadata="INSERT",
                                                                entropy_encoding="CABAC",
                                                                flicker_aq="ENABLED", framerate_control="SPECIFIED",
                                                                framerate_denominator=1, framerate_numerator=30,
                                                                gop_b_reference="ENABLED",
                                                                gop_closed_cadence=1, gop_num_b_frames=3, gop_size=60,
                                                                gop_size_units="FRAMES",
                                                                level="H264_LEVEL_AUTO", look_ahead_rate_control="HIGH",
                                                                num_ref_frames=3,
                                                                par_control="SPECIFIED", profile="HIGH",
                                                                rate_control_mode="CBR",
                                                                scan_type="PROGRESSIVE", scene_change_detect="ENABLED",
                                                                slices=1,
                                                                spatial_aq="ENABLED", syntax="DEFAULT",
                                                                temporal_aq="ENABLED",
                                                                timecode_insertion="DISABLED")
        video2_codec = medialive.CfnChannel.VideoCodecSettingsProperty(h264_settings=video2_h264)
        video2_description = medialive.CfnChannel.VideoDescriptionProperty(codec_settings=video2_codec, height=720,
                                                                           name="video_720p30", respond_to_afd="NONE",
                                                                           scaling_behavior="DEFAULT", sharpness=100,
                                                                           width=1280)

        """ Channel final settings and channel start """
        media_live_channel_timecode = medialive.CfnChannel.TimecodeConfigProperty(source="EMBEDDED")
        media_live_channel_encoder = medialive.CfnChannel.EncoderSettingsProperty(audio_descriptions=[audio1, audio2],
                                                                                  video_descriptions=[
                                                                                      video1_description,
                                                                                      video2_description],
                                                                                  output_groups=[output],
                                                                                  timecode_config=media_live_channel_timecode)

        policy_document = iam.PolicyDocument.from_json(INLINE_POLICY)
        medialive_role = iam.Role(scope=self,
                                  id='medialive_role',
                                  role_name='medialive_role',
                                  assumed_by=iam.ServicePrincipal('medialive.amazonaws.com'),
                                  managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                                      'AWSElementalMediaLiveFullAccess')],
                                  inline_policies={"medialivecustom": policy_document})

        media_live_channel = medialive.CfnChannel(scope=self,
                                                  id="media-live-channel-{0}".format(DEFAULT_CONF.get("id_channel")),
                                                  channel_class="SINGLE_PIPELINE", name=DEFAULT_CONF.get("id_channel"),
                                                  input_specification=media_live_channel_input_spec,
                                                  input_attachments=[media_live_channel_input_attach],
                                                  destinations=[media_live_channel_destination],
                                                  encoder_settings=media_live_channel_encoder,
                                                  role_arn=medialive_role.role_arn)

        # We need to add dependency because CFN must wait channel creation finish before starting the endpoint creation
        mediadep = core.ConcreteDependable()
        mediadep.add(channel)
        hls_endpoint.node.add_dependency(mediadep)
        media_live_channel.node.add_dependency(mediadep)
