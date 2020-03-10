from django.shortcuts import render
from .placesapi import search_places
import datetime
from .display_utils import *
import json
from collections import namedtuple
from pprint import pprint

Attraction = namedtuple('Attraction', ['places_id', 'lat', 'lon', 'score', 'is_restaurant'])
attr_info = namedtuple('attr_info', ['name', 'location'])


def home(request):
    return render(request, 'maps/home.html')


def survey(request):
    return render(request, 'maps/survey.html')


def loading(request):
    return render(request, 'maps/loading.html')


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

    start_in_time = datetime.datetime.strptime(
        survey_result['start_day'], "%I:%M %p")
    start_out_time = datetime.datetime.strftime(start_in_time, "%H:%M:%S")
    end_in_time = datetime.datetime.strptime(
        survey_result['end_day'], "%I:%M %p")
    end_out_time = datetime.datetime.strftime(end_in_time, "%H:%M:%S")

    hours = (start_out_time, end_out_time)
    hours_mod = (time_string_to_decimals(start_out_time),
                 time_string_to_decimals(end_out_time))
    k_attractions = survey_result['number_of_attractions']
    have_breakfast = False if survey_result['have_breakfast'] == 'No' else True
    k_restaurants = 3 if have_breakfast else 2

    # places api search
    radius = 50000
    api = 'AIzaSyB0Y13M5LBvl2gVR0c0eZVOyPAgBaEj8cs'
    attrs = search_places(str(lat) + ',' + str(lon),
                          radius, 'tourist_attraction', api)
    rests = search_places(str(lat) + ',' + str(lon), radius, 'restaurant', api)

    # format attrs and rests
    attrs_tup = attr_to_tup(attrs)
    rests_tup = attr_to_tup(rests, True)
    attrs_and_rests = attrs_tup + rests_tup

    # clustering
    attraction_list_clusters, centroids = clustering(
        num_days, have_breakfast, k_attractions, attrs_and_rests)
    # get hotel
    hotel_dict = find_hotel(centroids, api, radius)
    hotel_tup = attr_to_tup([hotel_dict], True)[0]

    # scheduling
    schedule = scheduling(attraction_list_clusters, int(
        k_attractions), k_restaurants, hotel_tup, hours_mod)

    placeid_dict = make_dict(attrs+rests)
    schedule_list = []
    tpa_list = []
    tpr_list = []
    hotel_name = hotel_dict['name']
    hotel_lat = hotel_dict['geometry']['location']['lat']
    hotel_lng = hotel_dict['geometry']['location']['lng']

    for schedule_day in schedule:
        schedule_list.append(schedule_day[0])
        tpa_list.append(schedule_day[1])
        tpr_list.append(schedule_day[2])

    map_waypoints = []
    map_day_waypoints = []
    for day in schedule_list:
        temp = []
        temp.append({'lat': hotel_lat, 'lng': hotel_lng, 'name': hotel_name})
        map_waypoints.append(
            {'lat': hotel_lat, 'lng': hotel_lng, 'name': hotel_name})
        for events in day:
            if isinstance(events, (int, float)):
                continue
            else:
                temp.append({'lat': events.lat, 'lng': events.lon,
                             'name': events.places_id})
                map_waypoints.append(
                    {'lat': events.lat, 'lng': events.lon, 'name': events.places_id})
        temp.append({'lat': hotel_lat, 'lng': hotel_lng, 'name': hotel_name})
        map_day_waypoints.append(temp)
    map_waypoints.append({'lat': hotel_lat, 'lng': hotel_lng, 'name': hotel_name})

    pprint(map_day_waypoints)

    events_list = format_schedule(start_date, end_date, placeid_dict, schedule_list,
                                  tpa_list, tpr_list, hotel_name, start_out_time, end_out_time)
    return render(request, 'maps/display.html', {'itinerary_in_json': json.dumps(events_list),
                                                 'location_list': json.dumps(map_waypoints),
                                                 'route_list': json.dumps(map_day_waypoints)})


def about(request):
    return render(request, 'maps/about.html', {'title': 'About'})
