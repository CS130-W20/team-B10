import random
import numpy as np
from collections import namedtuple


#####################################################################
# Attraction and Hotel Popping
#####################################################################
def attraction_popping(scores, attractions, num_attr, num_rest):
    # sort attractions by scores
    sorted_score_index = scores.argsort()[::-1]
    sorted_attractions = []
    for score_index in sorted_score_index:
        sorted_attractions.append(attractions[int(score_index)])
    top_k_attr_rest_idx = []
    # collect top k attractions and restaurants
    for a in sorted_attractions:
        idx = attractions.index(a)
        if a.is_restaurant == False and num_attr > 0:
            top_k_attr_rest_idx.append(idx)
            num_attr -= 1
        if a.is_restaurant == True and num_rest > 0:
            top_k_attr_rest_idx.append(idx)
            num_rest -= 1
    return top_k_attr_rest_idx


#####################################################################
# Single Day Scheduler
#####################################################################
def scheduler(scores, distances, attractions, num_attr, num_rest, hotel, hours):
    # get top attractions for the day
    top_k_attr_rest_idx = attraction_popping(scores, attractions, num_attr, num_rest)
    # calculate distance from hotel
    hotel_to_attraction = [abs((hotel.lat-a.lat))+abs((hotel.long-a.lon)) for a in top_k_attr_rest_idx]
    hotel_to_attraction_sorted = np.array(hotel_to_attraction).argsort()
    #find closest attraciton that is not a restaurant
    closest_attraction = None
    for a in hotel_to_attraction_sorted:
        if top_k_attr_rest_idx[a].is_restaurant == False:
            closest_attraction = top_k_attr_rest_idx.pop(a)
            break

    pass
