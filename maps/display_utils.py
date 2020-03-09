from collections import namedtuple
from .filter_scores import get_cluster_id_list, cluster_attraction_list
import datetime


attr_info = namedtuple('attr_info', ['name','location'])
Attraction = namedtuple('Attraction', ['places_id','lat','lon', 'score', 'is_restaurant'])
Hyperparameters = namedtuple('Hyperparameters', ['num_iter', 'neighborhood_frac', 'bias', 'random_max', 'random_min', 'decay'])


def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%m/%d/%Y")
    d2 = datetime.datetime.strptime(d2, "%m/%d/%Y")
    return abs((d2 - d1).days)


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
    # filtering configurations
    num_iter = 5000
    neighborhood_frac = 1.5
    bias = 10
    random_max = 5
    random_min = 1
    decay = 5e-2
    hyperparameters = Hyperparameters(num_iter, neighborhood_frac, bias, random_max, random_min, decay)

    # generate cluster by number of days
    cluster_id_list, centroids = get_cluster_id_list(attraction_list, num_days)
    attraction_list_clusters = cluster_attraction_list(cluster_id_list, attraction_list, num_days)

    return attraction_list_clusters, centroids


def format_schedule(start_date, end_date, placeid_dict, schedule_list, tpa_list, tpr_list, hotel_name, wake, sleep):
    events_list = []
    cur_time = datetime.datetime.strptime(start_date+"T"+wake, '%m/%d/%YT%H:%M:%S')
    start_date = cur_time.strftime('%Y-%m-%d')
    start = {'title': hotel_name, 'start':start_date+"T00:00:00", 'end':start_date+"T"+wake}
    events_list.append(start)
    day_num = 0
    for day in schedule_list:
        for events in day:
            if isinstance(events, (int, float)):
                cur_time += datetime.timedelta(hours=events)
            else:
                name = placeid_dict[events.places_id].name
                start_time = cur_time.strftime('%Y-%m-%dT%H:%M:%S')
                if events.is_restaurant:
                    cur_time += datetime.timedelta(hours=tpr_list[day_num])
                    name = 'Eat at: ' + name
                else:
                    cur_time += datetime.timedelta(hours=tpa_list[day_num])
                end_time = cur_time.strftime('%Y-%m-%dT%H:%M:%S')
                event = {'title': name, 'start':start_time, 'end':end_time}
                events_list.append(event)
        sleep_date = cur_time.strftime('%Y-%m-%d')
        cur_time += datetime.timedelta(days=1)
        wake_datetime = cur_time.strftime('%Y-%m-%d')+"T"+wake
        cur_time = datetime.datetime.strptime(wake_datetime, '%Y-%m-%dT%H:%M:%S')
        end_day = {'title': hotel_name, 'start':sleep_date+"T"+sleep, 'end':wake_datetime}
        events_list.append(end_day)
        day_num += 1
    return events_list

def make_dict(attrs):
    place_id = {'FREE': attr_info("Free Time", '')}
    for a in attrs:
        if 'name' not in a:
            a['name'] = ''
        if 'vicinity' not in a:
            a['vicinity'] = ''
        place_id[a['place_id']] = attr_info(a['name'], a['vicinity'])
    return place_id