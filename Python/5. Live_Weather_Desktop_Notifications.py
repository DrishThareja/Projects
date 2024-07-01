# Required url for the project
# 'https://wttr.in/{CITY}?format=%C+%t'

import requests
# it allows to send HTTP request easily

from plyer import notification
# it provides a way to send lotification on 
# various platforms like windows macOS, linux etc

import time
# use to handle time related task

CITY = 'Jaipur'
# Name of CITY you want to 
# know temperature by notification

def get_weather():
    url = f'https://wttr.in/{CITY}?format=%C+%t'
    # %C represents City
    # %t represents temperature

    response = requests.get(url)
    # send HTTP GET request

    weather_data = response.text.strip()
    # retrives the response 
    # text from the request

    return weather_data


# Fetch weather data and 
# display notification

def notify_weather():
    weather_data = get_weather()

    # Ensure that message is 
    # within the limit that is acceptable
    message = f'Weather in {CITY}: {weather_data}'
    
    if len(message) > 256:
        message = message[:252] + '...'
        # it will maintain the character till 252
        # after 252 character it will show ...


    # Notification
    notification.notify(
    title = 'Live Weather Update',
    message = message,
    timeout = 10
)

while True:
    try:
        notify_weather()
    except Exception as e:
        print(f'Error: {e}')

    time.sleep(5)
    # give the time you want after
    # which the notification will come
    # in seconds like 5 seconds

    # To stop the notification just close or kill the terminal