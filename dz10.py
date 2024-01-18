import sqlite3

import requests

from datetime import datetime

conn = sqlite3.connect('weather.db')

conn.execute('''CREATE TABLE IF NOT EXISTS weather

            (date TEXT, time TEXT, temperature REAL)''')

url = 'https://www.metaweather.com/api/location/924938/'

response = requests.get(url)

data = response.json()

now = datetime.now()

date = now.strftime('%Y-%m-%d')

time = now.strftime('%H:%M:%S')

temperature = data['consolidated_weather'][0]['the_temp']

conn.execute("INSERT INTO weather (date, time, temperature) VALUES (?, ?, ?)", (date, time, temperature))

conn.commit()

conn.close()