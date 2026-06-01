import requests
import json
import os

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
HISTORY_FILE = "history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def update_history(city):
    history = load_history()
    if city in history:
        history.remove(city)
    history.insert(0, city)
    save_history(history[:5])


def get_weather(city, url):
    try:
        response = requests.get(url, params={"q": city, "appid": API_KEY, "units": "metric"})
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.ConnectionError:
        print("No internet connection. Please check your network.")
        return None


def display_current(data):
    print("\n===== CURRENT WEATHER =====")
    print(f"City      : {data['name']}")
    print(f"Temperature: {data['main']['temp']}°C")
    print(f"Humidity  : {data['main']['humidity']}%")
    print(f"Condition : {data['weather'][0]['description'].capitalize()}")


def display_forecast(data):
    print("\n===== 5-DAY FORECAST =====")
    seen = set()
    for item in data["list"]:
        date, time = item["dt_txt"].split()
        # prefer noon reading for realistic daily temp
        if date not in seen and time == "12:00:00":
            seen.add(date)
            print(f"{date}  |  {item['main']['temp']}°C  |  {item['weather'][0]['description'].capitalize()}")
        if len(seen) == 5:
            break


def rain_warning(data):
    for item in data["list"][:8]:  # next 24 hours = 8 x 3hr slots
        if "rain" in item["weather"][0]["main"].lower():
            print("\n☔ Heads up — carry an umbrella tomorrow.")
            return
    print("\n✅ No rain expected in the next 24 hours.")


def choose_city():
    history = load_history()
    if history:
        print("\nRecent searches:")
        for i, city in enumerate(history, 1):
            print(f"  {i}. {city}")
        print("  0. Search a new city")

        choice = input("\nPick an option: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(history):
            return history[int(choice) - 1]

    city = input("Enter city name: ").strip()
    if not city:
        print("City name can't be empty.")
        return None
    return city


def main():
    print("==============================")
    print("     WEATHER FORECAST APP     ")
    print("==============================")

    city = choose_city()
    if not city:
        return

    current = get_weather(city, CURRENT_URL)
    if not current:
        print(f"Couldn't find weather data for '{city}'. Check the city name and try again.")
        return

    forecast = get_weather(city, FORECAST_URL)
    if not forecast:
        print("Forecast data unavailable right now.")
        return

    update_history(city)
    display_current(current)
    display_forecast(forecast)
    rain_warning(forecast)


if __name__ == "__main__":
    main()
