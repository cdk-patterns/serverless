import boto3
import time
import os
import csv
from datetime import datetime
import json

def main():
    event_bridge = boto3.client('events')
    # https://stackoverflow.com/questions/4906977/how-to-access-environment-variable-values

    data_s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
    data_s3_object_key  = os.environ.get('S3_OBJECT_KEY')

    if (None == data_s3_bucket_name
     or None == data_s3_object_key):
        print('ERROR: unable to retrieve environment variables (s3 bucket or object key, stream name')
        exit(1)

    print('Bucket Name ' + data_s3_bucket_name)
    print('S3 Object Key ' + data_s3_object_key)

    local_file = '/tmp/data.tsv'

    s3_resource = boto3.resource('s3')
    s3_resource.Object(data_s3_bucket_name, data_s3_object_key).download_file(local_file)

    print('SUCCESS: data file downloaded: ' + local_file)


    with open(local_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader)
        for row in reader:
            print(', '.join(row))
            event = {
                'status': 'extracted',
                'headers': ','.join(headers),
                'data': ','.join(row)
            }
            response = event_bridge.put_events(
                Entries=[
                    {
                        'DetailType': 's3RecordExtraction',
                        'EventBusName': 'default',
                        'Source': 'cdkpatterns.the-eventbridge-etl',
                        'Time': datetime.now(),
                        'Detail': json.dumps(event)
                        
                    },
                ]
            )
    exit(0)

if __name__ == '__main__':
    main()
