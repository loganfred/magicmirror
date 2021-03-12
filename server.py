from flask import Flask
from flask import jsonify
from flask import render_template
import os

import apis

app = Flask(__name__)

load_dotenv('config.env')

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


if os.getenv('DEBUG') == '1':
    extra_dirs = ['static',]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)
    app.run(extra_files=extra_files)
else:
    app.run()
