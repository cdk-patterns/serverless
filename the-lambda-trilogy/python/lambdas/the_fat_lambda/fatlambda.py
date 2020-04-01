def add(event, context):
    try:
        first_num = event["queryStringParameters"]['firstNum']
    except KeyError:
        first_num = 0

    try:
        second_num = event["queryStringParameters"]['secondNum']
    except KeyError:
        second_num = 0

    result = int(first_num) + int(second_num)
    print("The result of % s + % s = %s" % (first_num, second_num, result))
    return {'body': result, 'statusCode': 200}


def subtract(event, context):
    try:
        first_num = event["queryStringParameters"]['firstNum']
    except KeyError:
        first_num = 0

    try:
        second_num = event["queryStringParameters"]['secondNum']
    except KeyError:
        second_num = 0

    result = int(first_num) - int(second_num)
    print("The result of % s - % s = %s" % (first_num, second_num, result))
    return {'body': result, 'statusCode': 200}


def multiply(event, context):
    try:
        first_num = event["queryStringParameters"]['firstNum']
    except KeyError:
        first_num = 0

    try:
        second_num = event["queryStringParameters"]['secondNum']
    except KeyError:
        second_num = 0

    result = int(first_num) * int(second_num)
    print("The result of % s * % s = %s" % (first_num, second_num, result))
    return {'body': result, 'statusCode': 200}
