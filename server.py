from flask import Flask
from flask import jsonify
from flask import render_template

import apis

app = Flask(__name__)


@app.route('/api/bitcoin')
def bitcoin():
    return jsonify(apis.bitcoin())

@app.route('/api/weather')
def weather():
    return jsonify(apis.weather())

@app.route('/api/covid')
def covid():
    return jsonify(apis.covid())

@app.route('/api/chess')
def chess():
    return jsonify(apis.chess())

@app.route('/api/trivia')
def trivia():
    return jsonify(apis.trivia())

@app.route('/')
def index():
    return render_template('index.html')
