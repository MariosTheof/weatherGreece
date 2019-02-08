#the_weather/weather/views.py

import requests
import datetime as dt
from django.shortcuts import render
from geopy.geocoders import Nominatim
from .models import City
from .forms import CityForm


def weekday_setter():

    # get current day
    current_day = dt.date.today().isoweekday()

    today_m, today_tues, today_w, today_thur, today_fr, today_sat, today_sun = " ", " ", " ", " ", " ", " ", " "
    if current_day == 1: # today is Monday
        monday, tuesday, wednesday, thursday, friday, saturday, sunday = 0,1,2,3,4,5,6
        today_m = 'is_today' # in order
    elif current_day == 2: # today is Tuesday
        monday, tuesday, wednesday, thursday, friday, saturday, sunday = 6,0,1,2,3,4,5
        today_tues = 'is_today'
    elif current_day == 3: # today is Wednesday
        monday, tuesday, wednesday, thursday, friday, saturday, sunday = 5,6,0,1,2,3,4
        today_w = 'is_today'
    elif current_day == 4: # today is Thursday
        monday, tuesday, wednesday, thursday, friday, saturday, sunday = 4,5,6,0,1,2,3
        today_thur = 'is_today'
    elif current_day == 5: # today is Friday
        monday, tuesday, wednesday, thursday, friday, saturday, sunday = 3,4,5,6,0,1,2
        today_fr = 'is_today'
    elif current_day == 6: # today is Saturday
        monday, tuesday, wednesday, thursday, friday, saturday, sunday = 2,3,4,5,6,0,1
        today_sat = 'is_today'
    elif current_day == 7: # today is Sunday
        monday, tuesday, wednesday, thursday, friday, saturday, sunday = 1,2,3,4,5,6,0
        today_sun = 'is_today'


    return monday, tuesday, wednesday, thursday, friday, saturday, sunday, \
    today_m, today_tues, today_w, today_thur, today_fr, today_sat, today_sun

def index(request):

    # If something was typed in the serach bar, then do a
    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        if form.is_valid():
            # add postfix ",Greece" to ensure no ovelap with synonimities. eg. Athens, Georgia
            if ",Greece" in form.cleaned_data['name']:
                city = form.cleaned_data['name'] # city we want to predict
            else:
                city = form.cleaned_data['name'] + ',Greece'
            form = CityForm() # so the name does not stay after the search

    # GET method when the page is loaded and we want an empty form
    if request.method == 'GET':
        form = CityForm()
        city = 'Athens,Greece'


    # geolocator to get coordinates of places
    geolocator = Nominatim()
    location = geolocator.geocode(city)

    lat = str(location.latitude)
    lon = str(location.longitude)

    url = 'https://api.darksky.net/forecast/36b08b8c29fa105d710bd4c985dfff38/' + lat + ',' + lon + '?units=auto'
    response = requests.get(url) # request the API data and convert the JSON to Python data
    # convert requst to json
    json = response.json()

    date = dt.datetime.now().strftime("%d/%m/%Y")
    hour = dt.datetime.now().strftime("%H:%M")

    monday, tuesday, wednesday, thursday, friday, saturday, sunday, \
    today_m, today_tues, today_w, today_thur, today_fr, today_sat, today_sun = weekday_setter()
    weather_monday = {
        'city' : city,
        'today' : today_m,
        'day' : 'Monday',
        'temperatureHigh' : json['daily']['data'][monday]['temperatureHigh'],
        'temperatureLow' : json['daily']['data'][monday]['temperatureLow'],
        'summary' : json['daily']['data'][monday]['summary'],
        'icon' : json['daily']['data'][monday]['icon']
    }
    weather_tuesday = {
        'day' : 'Tuesday',
        'today' : today_tues,
        'temperatureHigh' : json['daily']['data'][tuesday]['temperatureHigh'],
        'temperatureLow' : json['daily']['data'][tuesday]['temperatureLow'],
        'summary' : json['daily']['data'][tuesday]['summary'],
        'icon' : json['daily']['data'][tuesday]['icon']
    }
    weather_wednesday = {
        'day' : 'Wednesday',
        'today' : today_w,
        'temperatureHigh' : json['daily']['data'][wednesday]['temperatureHigh'],
        'temperatureLow' : json['daily']['data'][wednesday]['temperatureLow'],
        'summary' : json['daily']['data'][wednesday]['summary'],
        'icon' : json['daily']['data'][wednesday]['icon']
    }
    weather_thursday = {
        'day' : 'Thursday',
        'today' : today_thur,
        'temperatureHigh' : json['daily']['data'][thursday]['temperatureHigh'],
        'temperatureLow' : json['daily']['data'][thursday]['temperatureLow'],
        'summary' : json['daily']['data'][thursday]['summary'],
        'icon' : json['daily']['data'][thursday]['icon']
    }
    weather_friday = {
        'day' : 'Friday',
        'today' : today_fr,
        'temperatureHigh' : json['daily']['data'][friday]['temperatureHigh'],
        'temperatureLow' : json['daily']['data'][friday]['temperatureLow'],
        'summary' : json['daily']['data'][friday]['summary'],
        'icon' : json['daily']['data'][friday]['icon']
    }
    weather_saturday = {
        'day' : 'Saturday',
        'today' : today_sat,
        'temperatureHigh' : json['daily']['data'][saturday]['temperatureHigh'],
        'temperatureLow' : json['daily']['data'][saturday]['temperatureLow'],
        'summary' : json['daily']['data'][saturday]['summary'],
        'icon' : json['daily']['data'][saturday]['icon']
    }
    weather_sunday = {
        'day' : 'Sunday',
        'today' : today_sun,
        'temperatureHigh' : json['daily']['data'][sunday]['temperatureHigh'],
        'temperatureLow' : json['daily']['data'][sunday]['temperatureLow'],
        'summary' : json['daily']['data'][sunday]['summary'],
        'icon' : json['daily']['data'][sunday]['icon']
    }

    curr_day ={
        'current_temperature' : json['currently']['temperature'],
        'icon' : json['currently']['icon'],
        'date' : date,
        'hour' : hour
    }

    context = { 'curr_day' : curr_day,
                'weather_monday' : weather_monday,
                'weather_tuesday' : weather_tuesday,
                'weather_wednesday' : weather_wednesday,
                'weather_thursday' : weather_thursday,
                'weather_friday' : weather_friday,
                'weather_saturday' : weather_saturday,
                'weather_sunday' : weather_sunday,
                'form' : form
    }


    return render(request, 'weather/index.html', context) #returns the index.html template


# https://api.darksky.net/forecast/36b08b8c29fa105d710bd4c985dfff38/37.8267,-122.4233
