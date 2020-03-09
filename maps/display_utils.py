from collections import namedtuple
from .placesapi import search_places
from .filter_scores import get_cluster_id_list, cluster_attraction_list, get_dists, filter_attraction_list
from .scheduling import scheduler
import datetime
import numpy as np


attr_info = namedtuple('attr_info', ['name','location'])
Attraction = namedtuple('Attraction', ['places_id','lat','lon', 'score', 'is_restaurant'])
Hyperparameters = namedtuple('Hyperparameters', ['num_iter', 'neighborhood_frac', 'bias', 'random_max', 'random_min', 'decay'])

# filtering configurations
num_iter = 5000
neighborhood_frac = 1.5
bias = 10
random_max = 5
random_min = 1
decay = 5e-2
hyperparameters = Hyperparameters(num_iter, neighborhood_frac, bias, random_max, random_min, decay)


def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%m/%d/%Y")
    d2 = datetime.datetime.strptime(d2, "%m/%d/%Y")
    return abs((d2 - d1).days)


def time_string_to_decimals(time_string):
    fields = time_string.split(":")
    hours = fields[0] if len(fields) > 0 else 0.0
    minutes = fields[1] if len(fields) > 1 else 0.0
    seconds = fields[2] if len(fields) > 2 else 0.0
    return float(hours) + (float(minutes) / 60.0) + (float(seconds) / pow(60.0, 2))


def attr_to_tup(attrs, is_rest=False):
    attr_tup = []
    for a in attrs:
        if 'name' not in a:
            a['name'] = ''
        if 'rating' not in a:
            a['rating'] = 0
        if is_rest == False:
            attr_tup.append(Attraction(a['name'], a['geometry']['location']['lat'], a['geometry']['location']['lng'], a['rating'], False))
        else:
            attr_tup.append(Attraction(a['name'], a['geometry']['location']['lat'], a['geometry']['location']['lng'], a['rating'], True))
    return attr_tup


def clustering(num_days, have_breakfast, k_attractions, attraction_list):
    k_restaurants = 3 if have_breakfast else 2
    # generate cluster by number of days
    cluster_id_list, centroids = get_cluster_id_list(attraction_list, num_days)
    attraction_list_clusters = cluster_attraction_list(cluster_id_list, attraction_list, num_days)

    return attraction_list_clusters, centroids


def scheduling(attraction_list_clusters, k_attractions, k_restaurants, hotel, hours):
    schedules = []
    for cluster in attraction_list_clusters:
        L = get_dists(cluster)
        l_avg = np.mean(L)
        # curate the score list of each cluster
        S = filter_attraction_list(cluster, L, l_avg, k_attractions, k_restaurants, hyperparameters)
        compile_schedule, tpa, tpr = scheduler(S, L, cluster, k_attractions, k_restaurants, hotel, hours)
        schedules.append((compile_schedule, tpa, tpr))
    return schedules


def format_schedule(start_date, end_date, attractions, schedule, tpa, tpr, hotel_name, wake, sleep):
    events_list = []

    start = {'title': hotel_name, 'start':start_date+"T00:00:00", 'end':start_date+"T"+wake}
    events_list.append(start)
    cur_time = datetime.datetime.strptime(start_date+"T"+wake, '%Y-%m-%dT%H:%M:%S')
    for day in schedule:
        for events in day:
            if isinstance(events, (int, float)):
                cur_time += datetime.timedelta(hours=events)
            else:
                name = attractions[events.places_id].name
                start_time = cur_time.strftime('%Y-%m-%dT%H:%M:%S')
                if events.is_restaurant:
                    cur_time += datetime.timedelta(hours=tpr)
                    name = 'Eat at: ' + name
                else:
                    cur_time += datetime.timedelta(hours=tpa)
                end_time = cur_time.strftime('%Y-%m-%dT%H:%M:%S')
                event = {'title': name, 'start':start_time, 'end':end_time}
                events_list.append(event)
        sleep_date = cur_time.strftime('%Y-%m-%d')
        cur_time += datetime.timedelta(days=1)
        wake_datetime = cur_time.strftime('%Y-%m-%d')+"T"+wake
        cur_time = datetime.datetime.strptime(wake_datetime, '%Y-%m-%dT%H:%M:%S')
        end_day = {'title': hotel_name, 'start':sleep_date+"T"+sleep, 'end':wake_datetime}
        events_list.append(end_day)
    return events_list


def find_hotel(centroids, api, radius):
    lat, lon = np.mean(centroids, axis=0)
    hotels = search_places(str(lat) + ',' + str(lon), radius, 'lodging', api)
    return hotels[0]
