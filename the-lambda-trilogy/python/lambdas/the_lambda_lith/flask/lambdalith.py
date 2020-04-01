import awsgi
from flask import (
    Flask,
    jsonify,
    request
)

app = Flask(__name__)


@app.route('/add')
def add():
    first_num = request.args.get('firstNum')
    if first_num is None:
        first_num = 0
    second_num = request.args.get('secondNum')
    if second_num is None:
        second_num = 0

    result = first_num + second_num
    return jsonify(status=200, message=result)


@app.route('/subtract')
def subtract():
    return jsonify(status=200, message='test')


@app.route('/multiply')
def multiply():
    return jsonify(status=200, message='test')


def handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})