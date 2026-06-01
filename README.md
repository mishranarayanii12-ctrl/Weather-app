# Weather CLI App

A command-line weather app that fetches live data using the OpenWeatherMap API.
Built this after getting tired of opening a browser just to check if I needed 
a jacket.

## Why I built this
Wanted to learn how APIs work in Python. The requests library and JSON parsing 
were new to me and this felt like a practical way to actually use them.

## What it does
- Enter any city name and get current temperature, humidity and weather condition
- Shows a 5-day forecast
- Warns you if rain is expected in the next 24 hours ("carry an umbrella tomorrow")
- Saves your last 5 searched cities so you don't retype them every time
- Handles errors without crashing — wrong city name, bad internet, API issues 
  all show clean messages instead of a wall of red text

## How to run it

git clone https://github.com/NarayaniMishra/weather-app
cd weather-app
pip install requests

Then add your API key:
- Sign up free at openweathermap.org
- Create a file called config.py and add: API_KEY = "your_key_here"

python weather.py

## API used
OpenWeatherMap free tier — Current Weather Data + 5 Day Forecast endpoints

## What I learned
- Making HTTP requests with the requests library
- Parsing nested JSON responses (the forecast response structure is messy)
- Storing and retrieving data from local files
- Writing proper error handling instead of letting the program crash

## Known issues
- Free API tier has a call limit so if you spam searches it'll stop working 
  for a bit
- City name matching isn't perfect — "Bengaluru" works but "Bangalore" 
  sometimes doesn't
