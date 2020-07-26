import os
import fcntl

MSG_FILE_PATH = '/mnt/msg/content'


def get_messages():
    try:
        with open(MSG_FILE_PATH, 'r') as msg_file:
            fcntl.flock(msg_file, fcntl.LOCK_SH)
            messages = msg_file.read()
            fcntl.flock(msg_file, fcntl.LOCK_UN)
    except:
        messages = 'No message yet.'
    return messages


def add_message(new_message):
    with open(MSG_FILE_PATH, 'a') as msg_file:
        fcntl.flock(msg_file, fcntl.LOCK_EX)
        msg_file.write(new_message + "\n")
        fcntl.flock(msg_file, fcntl.LOCK_UN)


def delete_messages():
    try:
        os.remove(MSG_FILE_PATH)
    except:
        pass


def lambda_handler(event, context):
    method = event['requestContext']['http']['method']
    if method == 'GET':
        messages = get_messages()
    elif method == 'POST':
        new_message = event['body']
        add_message(new_message)
        messages = get_messages()
    elif method == 'DELETE':
        delete_messages()
        messages = 'Messages deleted.'
    else:
        messages = 'Method unsupported.'
    return messages