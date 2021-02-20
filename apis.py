import os
import random
import requests
import datetime as dt
from dotenv import load_dotenv

load_dotenv('config.env')

def bitcoin():

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

    return dict(days=days,
                price=f'{price:,.2f}',
                profit=f'{profit:,.2f}',
                pct=f'{pct_growth:,.2f}')


def chess():

    username = os.getenv('CHESS_USERNAME')
    url = f'https://api.chess.com/pub/player/{username}'
    stats = requests.get(f'{url}/stats').json()['chess_daily']
    games = requests.get(f'{url}/games').json()['games']

    return dict(daily=stats['last']['rating'],
                peak=stats['best']['rating'],
                wins=stats['record']['win'],
                losses=stats['record']['loss'],
                drawn=stats['record']['draw'],
                active_count=len(games))

def weather():

    def convert(t):
        return dt.datetime.fromisoformat(t).strftime('%H:%M')

    url = 'https://www.metaweather.com/api/location'
    latlong = os.getenv('WEATHER_LAT_LONG')
    location = requests.get(f'{url}/search?lattlong={latlong}').json()[0]
    woeid = location['woeid']
    data = requests.get(f"{url}/{woeid}/").json()

    weather = data['consolidated_weather'][0]

    location = data['title']

    sun_up   = convert(data['sun_rise'])
    sun_down = convert(data['sun_set'])
    time     = convert(data['time'])

    state    = weather['weather_state_name']
    humidity = weather['humidity']

    high     = round(weather['max_temp'], 2)
    low      = round(weather['min_temp'], 2)
    temp     = round(weather['the_temp'], 2)

    temp_f = round(32 + 9 / 5 * temp, 2)
    low_f  = round(32 + 9 / 5 * high, 2)
    high_f = round(32 + 9 / 5 * low, 2)

    return dict(location=location,
                sunup=sun_up,
                sundown=sun_down,
                time=time,
                state=state,
                humidity=humidity,
                high=high,
                low=low,
                temp=temp,
                tempf=temp_f,
                lowf=low_f,
                highf=high_f)

def covid():

    state = os.getenv('COVID_STATE', 'FL')
    url = f'https://api.covidtracking.com/v1/states/{state}/current.json'

    covid = requests.get(url).json()

    return dict(deaths=covid['death'],
                hospitalized=covid['hospitalizedCurrently'],
                icued=covid['inIcuCurrently'],
                state=state)


def trivia():

    # obtain categories and their ids
    url = 'https://opentdb.com/api.php'

    results = requests.get(url, params=dict(category=9, amount=1)).json()

    result = results['results'][0]

    answers = result['incorrect_answers'] + [result['correct_answer']]
    answers = answers[:]
    random.shuffle(answers)

    return dict(question=result['question'],
                answers=answers,
                correct=result['correct_answer'],
                difficulty=result['difficulty'])
