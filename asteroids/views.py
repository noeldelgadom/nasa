from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def index(request):
    all_list = []
    date = '2015-09-07'
    all_list += each_day(date)
    date = '2015-09-08'
    all_list += each_day(date)
    d = {'key': all_list}
    return render(request, 'index.html', d)

def each_day(date):
    API_KEY = 'ZukoKlwpEqm4xElQVViwo75RfJ32tzgX4gGCIZdU'
    r = requests.get('https://api.nasa.gov/neo/rest/v1/feed?start_date='+ date +'&end_date=' + date + '&api_key=' + API_KEY)
    json_object = r.json()
    asteroid_count = json_object['element_count']
    asteroid_list = []
    for i in range(asteroid_count):
        name = json_object['near_earth_objects'][date][i]['name']
        name = name[:-1]
        a = {
            'name' : name[1:],
            'date' : date,
            'diameter_min' : json_object['near_earth_objects'][date][i]['estimated_diameter']['kilometers']['estimated_diameter_min'],
            'diameter_max' : json_object['near_earth_objects'][date][i]['estimated_diameter']['kilometers']['estimated_diameter_max'],
            'url' : json_object['near_earth_objects'][date][i]['nasa_jpl_url'],
            'hazardous' : json_object['near_earth_objects'][date][i]['is_potentially_hazardous_asteroid'],
            }
        asteroid_list.append(a)
    return asteroid_list
