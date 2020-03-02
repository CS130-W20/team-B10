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
    pass
