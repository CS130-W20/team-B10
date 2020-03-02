import random
import numpy as np
from collections import namedtuple

#####################################################################
# Attraction and Hotel Popping
#####################################################################
def attraction_popping(scores, attractions, num_attr, num_rest):
    #sort attractions by scores
    sorted_score_index = scores.argsort()[::-1]
    sorted_attractions = attractions[sorted_score_index]
    top_k_attr_rest_idx = []
    #collect top k attractions and restaurants
    for a in sorted_attractions:
        idx = attractions.index(a)
        if a.is_rest == False and num_attr > 0:
            top_k_attr_rest.append(idx)
            num_attr -= 1
        if a.is_rest == True and num_rest > 0:
            top_k_attr_rest.append(idx)
            num_rest -= 1
    return top_k_attr_rest_idx
