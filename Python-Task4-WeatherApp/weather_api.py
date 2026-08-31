import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        print("Request timed out. Please check your internet connection.")
        return None

    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            print("City not found. Please check the city name.")
            return None

        elif response.status_code == 401:
            print("Invalid API key.")
            return "INVALID_KEY"

        else:
            print(f"API error: {response.status_code}")
            return None

    except requests.exceptions.RequestException:
        print("Unable to connect to the weather service.")
        return None


def extract_weather_data(data):
    temperature = data["main"]["temp"]
    temperature_f = (temperature * 9 / 5) + 32
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]
    city_name = data["name"]

    return (
        temperature,
        temperature_f,
        humidity,
        description,
        wind_speed,
        city_name
    )


while True:
    city = input("Enter a city name or ZIP code: ").strip()

    if not city:
        print("City name cannot be empty. Please try again.")
        continue

    data = get_weather(city)

    if data == "INVALID_KEY":
        break

    if data is None:
        continue

    break


if data != "INVALID_KEY":
    (
        temperature,
        temperature_f,
        humidity,
        description,
        wind_speed,
        city_name
    ) = extract_weather_data(data)

    print("\nWeather Information")
    print("-------------------")
    print("City:", city_name)
    print("Temperature:", round(temperature, 1), "°C")
    print("Temperature:", round(temperature_f, 1), "°F")
    print("Humidity:", humidity, "%")
    print("Condition:", description.title())
    print("Wind Speed:", wind_speed, "m/s")