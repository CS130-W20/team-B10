from collections import namedtuple
from .filter_scores import get_cluster_id_list, cluster_attraction_list
from datetime import datetime

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%m/%d/%Y")
    d2 = datetime.strptime(d2, "%m/%d/%Y")
    return abs((d2 - d1).days)


def attr_to_tup(attrs, is_rest=False):
    Attraction = namedtuple('Attraction', ['places_id','lat','lon', 'score', 'is_restaurant'])
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
    Hyperparameters = namedtuple('Hyperparameters', ['num_iter', 'neighborhood_frac', 'bias', 'random_max', 'random_min', 'decay'])
    hyperparameters = Hyperparameters(num_iter, neighborhood_frac, bias, random_max, random_min, decay)

    # generate cluster by number of days
    cluster_id_list, centroids = get_cluster_id_list(attraction_list, num_days)
    attraction_list_clusters = cluster_attraction_list(cluster_id_list, attraction_list, num_days)

    return attraction_list_clusters, centroids
