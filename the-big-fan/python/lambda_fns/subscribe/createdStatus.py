import json
import logging

def handler(event, context):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info("request: " + json.dumps(event))

    records = event["Records"]
    
    for record in records:
        payload = record["body"]
        logger.info("received message " + payload)