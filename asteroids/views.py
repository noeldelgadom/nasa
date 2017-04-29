from django.shortcuts import render
from django.http import HttpResponse
from datetime import date,timedelta
import requests

# Create your views here.
def index(request):
    start_date = '2015-09-07'
    end_date = '2015-09-09'
    date_str_list = build_dates(start_date, end_date)

    all_asteroid_list = []
    for i in date_str_list:
        all_asteroid_list += each_day(i)
    d = {'asteroids': all_asteroid_list,
        'dates': date_str_list
    }
    return render(request, 'index.html', d)

def each_day(date_now):
    API_KEY = 'ZukoKlwpEqm4xElQVViwo75RfJ32tzgX4gGCIZdU'
    r = requests.get('https://api.nasa.gov/neo/rest/v1/feed?start_date='+ date_now +'&end_date=' + date_now + '&api_key=' + API_KEY)
    json_object = r.json()
    asteroid_count = json_object['element_count']
    asteroid_list = []
    for i in range(asteroid_count):
        name = json_object['near_earth_objects'][date_now][i]['name']
        name = name[:-1]
        a = {
            'name' : name[1:],
            'date' : date_now,
            'diameter_min' : json_object['near_earth_objects'][date_now][i]['estimated_diameter']['kilometers']['estimated_diameter_min'],
            'diameter_max' : json_object['near_earth_objects'][date_now][i]['estimated_diameter']['kilometers']['estimated_diameter_max'],
            'url' : json_object['near_earth_objects'][date_now][i]['nasa_jpl_url'],
            'hazardous' : json_object['near_earth_objects'][date_now][i]['is_potentially_hazardous_asteroid'],
            }
        asteroid_list.append(a)
    return asteroid_list

def build_dates(start_date_str, end_date_str):
    date_str_list = []
    start_date_dt = date(*map(int, start_date_str.split('-')))
    end_date_dt = date(*map(int, end_date_str.split('-')))

    while end_date_dt.isoformat() not in date_str_list:
        date_str_list.append(start_date_dt.isoformat())
        start_date_dt += timedelta(days=1)
    return date_str_list
