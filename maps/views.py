from django.shortcuts import render
from .placesapi import search_places
from datetime import datetime
from .display_utils import *
import json

def home(request):
    return render(request, 'maps/home.html')

def maps(request):
    return render(request, 'maps/maps.html')

def survey(request):
    return render(request, 'maps/survey.html')

def display(request):
    # NEEDS: VALIDATION/DEFUALT VALUES
    # get data from url
    dest_and_dates = json.loads(request.GET['dest_and_dates'])
    survey_result = json.loads(request.GET['survey_result'])

    destination = dest_and_dates['destination']
    lat = dest_and_dates['cityLat'][0]
    lon = dest_and_dates['cityLng'][0]
    start_date = dest_and_dates['date'][0]
    end_date = dest_and_dates['date'][1]
    num_days = days_between(start_date, end_date)

    start_in_time = datetime.strptime(survey_result['start_day'], "%I:%M %p")
    start_out_time = datetime.strftime(start_in_time, "%H:%M:%S")
    end_in_time = datetime.strptime(survey_result['end_day'], "%I:%M %p")
    end_out_time = datetime.strftime(end_in_time, "%H:%M:%S")

    hours = (start_out_time, end_out_time)
    k_attractions = survey_result['number_of_attractions']
    have_breakfast = survey_result['have_breakfast']

    # places api search
    radius = 16093
    api = 'AIzaSyB0Y13M5LBvl2gVR0c0eZVOyPAgBaEj8cs'
    attrs = search_places(str(lat) + ',' + str(lon), radius, 'tourist_attraction', api)
    rests = search_places(str(lat) + ',' + str(lon), radius, 'restaurant', api)
    hotels = search_places(str(lat) + ',' + str(lon), radius, 'lodging', api)

    # format attrs and rests
    attrs_tup = attr_to_tup(attrs)
    rests_tup = attr_to_tup(rests, True)
    attrs_and_rests = attrs_tup + rests_tup

    # clustering
    attraction_list_clusters, centroids = clustering(num_days, have_breakfast, k_attractions, attrs_and_rests)

    pass
    events_list = []
    event1 = {'title': 'Testing', 'start':'2020-03-14T11:00:00', 'start':'2020-03-14T12:00:00'}
    event2 = {'title': 'Test2', 'start':'2020-03-16T11:00:00', 'start':'2020-03-16T12:00:00'}
    events_list.append(event1)
    events_list.append(event2)
    return render(request, 'maps/display.html', {'itinerary_in_json': json.dumps(events_list)})

def about(request):
    return render(request, 'maps/about.html', {'title': 'About'})
