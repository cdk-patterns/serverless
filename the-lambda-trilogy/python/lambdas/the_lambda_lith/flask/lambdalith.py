import awsgi
from flask import (
    Flask,
    jsonify,
)

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify(status=200, message='OK')


@app.route('/test')
def test():
    return jsonify(status=200, message='test')


def handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})