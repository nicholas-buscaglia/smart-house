import datetime
import pytz
import requests
import json

def get_current_time(location=None):
    """
    Gets the current time in the specified location or local timezone if no location is provided.

    :param location: The location to get the current time in (e.g. 'New York')
    :return: A datetime object representing the current time
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
        tz = pytz.localtimezone()
        current_time = datetime.datetime.now(tz)

    return current_time

# Get the current time in either local timezone or a specified location
location = input("Enter location (default: current timezone): ")

if location:
    time = get_current_time(location)
    if time:
        print(f"{location} Time: {time}")
else:
    local_time = get_current_time()
    print(f"Local Time: {local_time}")
