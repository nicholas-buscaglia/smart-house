import datetime
import pytz
import requests
import json

def get_current_time(location=None):
    """
    Gets the current time in the specified location or local timezone if no location is provided.

    :param location: The location to get the current time in (e.g. 'New York')
    :return: A string representing the current time in the format "11:23AM"
    """
    if location:
        url = f'http://worldtimeapi.org/api/timezone/{location.replace(" ", "_")}'
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            tz = pytz.timezone(data['timezone'])
            current_time = datetime.datetime.fromtimestamp(data['unixtime'], tz)
        else:
            print(f"Error: Could not get time for location '{location}'")
            current_time = None
    else:
        tz = pytz.timezone('America/New_York')
        current_time = datetime.datetime.now(tz)

    current_time_str = current_time.strftime("%I:%M%p")
    print(f'current time: {current_time_str}')

    return current_time_str


def get_current_date(location=None):
    """
    Gets the current date in the specified location or local timezone if no location is provided.

    :param location: The location to get the current date in (e.g. 'New York')
    :return: A string representing the current date in the format "January 1, 2023"
    """
    if location:
        url = f'http://worldtimeapi.org/api/timezone/{location.replace(" ", "_")}'
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            tz = pytz.timezone(data['timezone'])
            current_date = datetime.datetime.fromtimestamp(data['unixtime'], tz).date()
        else:
            print(f"Error: Could not get time for location '{location}'")
            current_date = None
    else:
        tz = pytz.timezone('EST')
        current_date = datetime.datetime.now(tz).date()

    formatted_date = current_date.strftime("%B %d, %Y")
    print(f'current date: {formatted_date}')

    return formatted_date
