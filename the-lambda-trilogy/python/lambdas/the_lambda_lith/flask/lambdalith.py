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
    return jsonify(status=200, message=result)


@app.route('/subtract')
def subtract():
    return jsonify(status=200, message='test')


@app.route('/multiply')
def multiply():
    return jsonify(status=200, message='test')


def handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})