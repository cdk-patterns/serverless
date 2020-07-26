import json

def handler(event, context):
    print("Event: %s" % (json.dumps(event)))