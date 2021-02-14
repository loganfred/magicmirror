from flask import Flask
from flask import jsonify
from flask import render_template

from apis import Bitcoin
from apis import Chess
from apis import Covid
from apis import Trivia
from apis import Weather

app = Flask(__name__)


@app.route('/')
def index():

    bitcoin = Bitcoin()
    chess = Chess()
    covid = Covid()
    trivia = Trivia()
    weather = Weather()

    items = dict(bitcoin=bitcoin,
                 chess=chess,
                 covid=covid,
                 trivia=trivia,
                 weather=weather)

    return render_template('index.html', **items)
