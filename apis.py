import os
import random
import requests
import datetime as dt
from dotenv import load_dotenv

load_dotenv('config.env')

class Bitcoin:

    def __init__(self):

        owned = float(os.getenv('BITCOIN_AMOUNT'))
        principle = float(os.getenv('BITCOIN_PRINCIPLE'))
        purchase = dt.datetime.fromisoformat(os.getenv('BITCOIN_PURCHASE'))

        url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
        data = requests.get(url).json()

        price = data['bpi']['USD']['rate_float']
        timestamp = dt.datetime.fromisoformat(data['time']['updatedISO'])

        profit = (price * owned - principle)
        pct_growth = profit / principle * 100
        days = (timestamp.replace(tzinfo=None) - purchase).days

        self.days = days
        self.price = f'{price:,.2f}'
        self.profit = f'{profit:,.2f}'
        self.growth_pct = f'{pct_growth:,.2f}'


class Chess:

    def __init__(self):

        username = os.getenv('CHESS_USERNAME')
        url = f'https://api.chess.com/pub/player/{username}'
        stats = requests.get(f'{url}/stats').json()['chess_daily']
        games = requests.get(f'{url}/games').json()['games']

        self.daily = stats['last']['rating']
        self.peak = stats['best']['rating']
        self.wins = stats['record']['win']
        self.losses = stats['record']['loss']
        self.drawn = stats['record']['draw']
        self.active_count = len(games)

class Weather:

    def __init__(self):

        url = 'https://www.metaweather.com/api/location'
        latlong = os.getenv('WEATHER_LAT_LONG')
        location = requests.get(f'{url}/search?lattlong={latlong}').json()[0]
        woeid = location['woeid']
        data = requests.get(f"{url}/{woeid}/").json()

        weather = data['consolidated_weather'][0]

        self.location = data['title']

        self.sun_up   = self.convert(data['sun_rise'])
        self.sun_down = self.convert(data['sun_set'])
        self.time     = self.convert(data['time'])

        self.state    = weather['weather_state_name']
        self.humidity = weather['humidity']

        self.high     = round(weather['max_temp'], 2)
        self.low      = round(weather['min_temp'], 2)
        self.temp     = round(weather['the_temp'], 2)

        self.temp_f = self.c_to_f(self.temp)
        self.low_f  = self.c_to_f(self.high)
        self.high_f = self.c_to_f(self.low)

    def c_to_f(self, t):
        return round(32 + 9 / 5 * t, 2)

    def convert(self, t):
        return dt.datetime.fromisoformat(t).strftime('%H:%M')

class Covid:

    def __init__(self):

        state = os.getenv('COVID_STATE', 'FL')
        url = f'https://api.covidtracking.com/v1/states/{state}/current.json'

        covid = requests.get(url).json()

        self.deaths = covid['death']
        self.hospitalized = covid['hospitalizedCurrently']
        self.icued = covid['inIcuCurrently']
        self.state = state


class Trivia:

    def __init__(self):

        # obtain categories and their ids
        url = 'https://opentdb.com/api.php'

        results = requests.get(url, params=dict(category=9, amount=1)).json()

        result = results['results'][0]

        answers = result['incorrect_answers'] + [result['correct_answer']]
        self.answers = answers[:]
        random.shuffle(self.answers)

        self.question = result['question']
        self.correct = result['correct_answer']
        self.difficulty = result['difficulty']
