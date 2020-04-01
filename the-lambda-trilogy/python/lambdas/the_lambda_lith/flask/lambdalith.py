import awsgi
from flask import (
    Flask,
    jsonify,
    request
)

app = Flask(__name__)


@app.route('/add')
def add():
    first_num = request.args.get('firstNum', default=0, type=int)
    second_num = request.args.get('secondNum', default=0, type=int)

    result = first_num + second_num
    print("The result of % s + % s = %s" % (first_num, second_num, result))
    return jsonify(result=result)


@app.route('/subtract')
def subtract():
    first_num = request.args.get('firstNum', default=0, type=int)
    second_num = request.args.get('secondNum', default=0, type=int)

    result = first_num - second_num
    print("The result of % s - % s = %s" % (first_num, second_num, result))
    return jsonify(result=result)


@app.route('/multiply')
def multiply():
    first_num = request.args.get('firstNum', default=0, type=int)
    second_num = request.args.get('secondNum', default=0, type=int)

    result = first_num * second_num
    print("The result of % s x % s = %s" % (first_num, second_num, result))
    return jsonify(result=result)


def handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})
