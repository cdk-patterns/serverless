import boto3
import time
import os
import csv

def SendData(client, stream_name, data_binary_string):
    response = client.put_record(
        DeliveryStreamName=stream_name,
        Record={'Data': data_binary_string}
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('SUCCESS: your request ID is : ' + response['ResponseMetadata']['RequestId'])

    else:
        print('ERROR: something went wrong')
        exit(1)

def main():
    # https://stackoverflow.com/questions/4906977/how-to-access-environment-variable-values

    data_s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
    data_s3_object_key  = os.environ.get('S3_OBJECT_KEY')
    stream_name         = os.environ.get('STREAM_NAME')

    if (None == data_s3_bucket_name
     or None == data_s3_object_key
     or None == stream_name):
        print('ERROR: unable to retrieve environment variables (s3 bucket or object ket, stream name')
        exit(1)

    local_file = '/tmp/data.tsv'

    s3_resource = boto3.resource('s3')
    s3_resource.Object(data_s3_bucket_name, data_s3_object_key).download_file(local_file)

    print('SUCCESS: data file downloaded: ' + local_file)

    firehose = boto3.client('firehose')
    with open(local_file) as f:
        for line in f:
            binary_string = str.encode(line)
            SendData(firehose, stream_name, binary_string)

    print('SUCCESS: sending data finished')
    exit(0)

if __name__ == '__main__':
    main()
