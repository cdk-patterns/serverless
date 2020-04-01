def add(event, context):
    first_num = event["queryStringParameters"]['firstNum']
    if first_num is None:
        first_num = 0

    second_num = event["queryStringParameters"]['secondNum']
    if second_num is None:
        second_num = 0

    result = int(first_num) + int(second_num)
    print("The result of % s + % s = %s" % (first_num, second_num, result))
    return {'body': result, 'statusCode': 200}