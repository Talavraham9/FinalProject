import flask
from flask import Flask, json
from markupsafe import escape
from flask import jsonify


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/connect", methods=['GET'])
def connect():
    response = flask.jsonify({'data': 'Connected successfully'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


@app.route("/frame", methods=['GET'])
def frame_response():
    response = flask.jsonify({'sever': "1", "obj": "car"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__=='__main__':
    app.run(host='192.168.1.235', port=5000)