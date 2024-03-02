import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'

def fetch_weather(location, units='metric'):
    try:
        url = f"{BASE_URL}q={location}&appid={API_KEY}&units={units}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def display_weather(data):
    try:
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        print(f"Temperature: {temp}°C")
        print(f"Weather: {description}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
    except KeyError:
        print("Error: Could not parse weather data.")

def main():
    location = input("Enter the name of a city or a ZIP code: ")
    units = input("Choose temperature units - Celsius (C) or Fahrenheit (F): ").lower()
    units_format = 'metric' if units == 'c' else 'imperial'

    weather_data = fetch_weather(location, units_format)
    if weather_data:
        display_weather(weather_data)

if __name__ == "__main__":
    main()
