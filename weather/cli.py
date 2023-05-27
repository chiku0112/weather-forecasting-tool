from typing import Optional
from datetime import datetime, timezone
import requests
import typer
from weather import ERRORS, __app_name__, __version__
import warnings
import os
from dotenv import load_dotenv

app = typer.Typer()

# DEFINE BASE_URL AND API_KEY
BASE_URL = "https://api.openweathermap.org/data/2.5"

# load the API key from the .env file
load_dotenv("weather/sample.env")
API_KEY = os.getenv("API_KEY")

warnings.filterwarnings('ignore')

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return

@app.command()
def city(
    city: str = typer.Argument(...)
) -> None:
    """Add a new city with a DESCRIPTION."""
    weather_data = _get_weather_data(city=city)
    print_weather_data(weather_data)


# create a get weather function that takes in a city as an argument and returns the weather data using the OpenWeatherMap API
def _get_weather_data(city: str) -> dict:
    # """Get weather data from OpenWeatherMap API."""
    url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise typer.Exit(message=f"Error: {response.status_code}")


# define a function that will print the weather data
def print_weather_data(data: dict) -> None:
    # """Print weather data to the console."""
    typer.secho("""
______________________________________________
                    
Welcome to Weather-GPT! It's {0} right now!
______________________________________________
    """.format(datetime.now().strftime("%H:%M:%S")), fg=typer.colors.YELLOW, bold=True)

    city_name = data["name"]
    country_code = data["sys"]["country"]
    weather = data["weather"][0]["main"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    temp_min = data["main"]["temp_min"]
    temp_max = data["main"]["temp_max"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    wind_deg = data["wind"]["deg"]
    sunrise = data["sys"]["sunrise"]
    sunset = data["sys"]["sunset"]

    typer.secho(f"Weather for {city_name}, {country_code}:\n", fg=typer.colors.GREEN, bold=True)

    if weather == "Clouds":
        print("☁️☁️  It's cloudy ☁️☁️\n")
    elif weather == "Rain":
        print("🌧️  It's raining 🌧️\n")
    elif weather == "Snow":
        print("❄️  It's snowing ❄️\n")
    elif weather == "Clear":
        print("☀️  The sky is clear ☀️\n")
    elif weather == "Humid":
        print("💧  It's humid 💧\n")
    elif weather == "Haze":
        print("~ It's hazy ~\n")

    # convert temperature from Kelvin to Celsius
    temp = temp - 273.15
    feels_like = feels_like - 273.15
    temp_min = temp_min - 273.15
    temp_max = temp_max - 273.15

    # round off the temperatures to 2 decimal places
    temp = round(temp, 2)
    feels_like = round(feels_like, 2)
    temp_min = round(temp_min, 2)
    temp_max = round(temp_max, 2)

    print(f"Temperature: {temp}°C\nFeels like: {feels_like}°C\nLow: {temp_min}°C\nHigh: {temp_max}°C")
    print(f"Humidity: {humidity}%\nWind Speed: {wind_speed} meter/sec\nWind Direction: {wind_deg}°")
    print("\nThe sun rose at {0} and will set at {1}.".format(datetime.fromtimestamp(sunrise+19800, tz=timezone.utc).strftime("%H:%M:%S"), datetime.fromtimestamp(sunset+19800, tz=timezone.utc).strftime("%H:%M:%S")))
    print("______________________________________________")
    print("\n")