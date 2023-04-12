import os
import requests
import json


def get_local_weather():
    """
    Gets the local weather using the OpenWeatherMap API.

    :return: A dictionary containing weather information
    """
    # Get the API key from an environment variable
    api_key = os.environ.get('IPIFY_API_KEY')

    # Use the ipify API to get the user's public IP address
    response = requests.get('https://api.ipify.org?format=json')
    ip_address = response.json()['ip']

    # Get the API key from an environment variable
    api_key = os.environ.get('IPSTACK_API_KEY')

    # Use the ipstack API to get the user's location information
    response = requests.get(f'http://api.ipstack.com/{ip_address}?access_key={api_key}')
    location = response.json()

    # Check if the latitude and longitude keys exist in the location dictionary
    if 'latitude' not in location or 'longitude' not in location:
        print("Unable to get location information")
        return None

    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')

    # Use the OpenWeatherMap API to get the local weather
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={location["latitude"]}&lon={location["longitude"]}&appid={api_key}&units=imperial')
    current_weather_data = response.json()

    # Use the OpenWeatherMap API to get the local weather forecast
    response = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={location["latitude"]}&lon={location["longitude"]}&appid={api_key}')
    forecast_data = response.json()

    # Extract relevant weather information
    weather = {}
    weather['location'] = location['city'] + ', ' + location['region_name'] + ', ' + location['country_name']
    weather['current_description'] = current_weather_data['weather'][0]['description']
    weather['current_temperature'] = current_weather_data['main']['temp']
    weather['current_humidity'] = current_weather_data['main']['humidity']
    weather['current_wind_speed'] = current_weather_data['wind']['speed']

    # Get the weather forecast for the next 5 days
    forecast = []
    for forecast_item in forecast_data['list'][:40:8]:
        forecast_dict = {}
        forecast_dict['date'] = forecast_item['dt_txt']
        forecast_dict['description'] = forecast_item['weather'][0]['description']
        forecast_dict['temperature'] = forecast_item['main']['temp']
        forecast_dict['humidity'] = forecast_item['main']['humidity']
        forecast_dict['wind_speed'] = forecast_item['wind']['speed']
        forecast.append(forecast_dict)

    weather['forecast'] = forecast
    # print(weather)

    weather = f"""{weather['location']}: Currently {weather['current_description']}, 
    the temperature is {weather['current_temperature']} degrees with {weather['current_humidity']} percent humidity and 
    wind speeds of {weather['current_wind_speed']} miles per hour"""

    return weather
