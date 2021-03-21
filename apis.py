import os
import re
import csv
import html
import random
import requests
from dotenv import load_dotenv
from datetime import datetime as dt

load_dotenv('config.env')

def bitcoin():

    if os.getenv('DEBUG') == '1':
        return dict(days='100',
                    price='50,000.00',
                    profit='3,000.00',
                    pct=f'100.00')

    owned = float(os.getenv('BITCOIN_AMOUNT'))
    principle = float(os.getenv('BITCOIN_PRINCIPLE'))
    purchase = dt.fromisoformat(os.getenv('BITCOIN_PURCHASE'))

    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    data = requests.get(url).json()

    price = data['bpi']['USD']['rate_float']
    timestamp = dt.fromisoformat(data['time']['updatedISO'])

    profit = (price * owned - principle)
    pct_growth = profit / principle * 100
    days = (timestamp.replace(tzinfo=None) - purchase).days

    return dict(days=days,
                price=f'{price:,.2f}',
                profit=f'{profit:,.2f}',
                pct=f'{pct_growth:,.2f}')


def chess():

    if os.getenv('DEBUG') == '1':
        return dict(daily=700,
                    peak=700,
                    wins=10,
                    losses=10,
                    drawn=1,
                    active_count=3)

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
        return dt.fromisoformat(t).strftime('%H:%M')

    if os.getenv('DEBUG') == '1':
        return dict(location='Washington DC',
                    sunup='7:00',
                    sundown='17:00',
                    time='12:00',
                    state='FL',
                    humidity='70.00',
                    high='25',
                    low='20',
                    temp='23',
                    tempf='60',
                    lowf='50',
                    highf='70')

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
    low_f  = round(32 + 9 / 5 * low, 2)
    high_f = round(32 + 9 / 5 * high, 2)

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

    if os.getenv('DEBUG') == '1':

        return dict(deaths='10,000',
                    hospitalized='1,000',
                    icued='50',
                    state='FL')

    state = os.getenv('COVID_STATE', 'FL')
    url = f'https://api.covidtracking.com/v1/states/{state}/current.json'

    covid = requests.get(url).json()

    return dict(deaths=covid['death'],
                hospitalized=covid['hospitalizedCurrently'],
                icued=covid['inIcuCurrently'],
                state=state)


def trivia():

    if os.getenv('DEBUG') == '1':

        return dict(question='How many answers are there?',
                    answers=['One', 'Two', 'Three', 'Four'],
                    correct='Four',
                    difficulty='Easy')

    # obtain categories and their ids
    url = 'https://opentdb.com/api.php'

    results = requests.get(url, params=dict(category=9, amount=1)).json()

    result = results['results'][0]

    answers = result['incorrect_answers'] + [result['correct_answer']]
    answers = answers[:]
    random.shuffle(answers)

    return dict(question=html.unescape(result['question']),
                answers=[html.unescape(x) for x in answers],
                correct=html.unescape(result['correct_answer']),
                difficulty=result['difficulty'])

def birthdays(only_this_month=False):
    if os.getenv('DEBUG') == '1':
        return dict(birthdays=[{'Me': 'April 1'}, {'You': 'April 2'}])

    with open('birthdays.csv') as b:
        reader = csv.reader(b, delimiter='\t')
        data = [x for x in reader]

    if only_this_month:
        month = dt.now().strftime('%B')
        re_m = re.compile('(\w+) (\d+)')

        filtered = []
        for date, name in data:
            if re.match(re_m, date).groups()[0] == month:
                filtered.append([date, name])

        return filtered

    return data
