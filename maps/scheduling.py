import random
import numpy as np
from collections import namedtuple
from filter_scores import gen_syn_loc, get_dists, filter_attraction_list, Hyperparameters


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
def next_loc(attr, distance, attrs, new_top_k_attr, is_rest):
    #find next closest location
    distance_sort = distance.argsort()
    attractions_sort = [attrs[i] for i in distance_sort]
    attraction = None
    for i in attractions_sort:
        if i != attr and i.is_restaurant == is_rest and i in new_top_k_attr:
            attraction = new_top_k_attr.pop(new_top_k_attr.index(i))
            break
    return attraction, new_top_k_attr, distance[attrs.index(attraction)]


def compile(time, attraction):
    #compile time and attractions
    final = []
    for t in range(len(time)):
        final.append(time[t])
        if t < len(attraction):
            final.append(attraction[t])
    return final


def scheduler(scores, distances, attractions, num_attr, num_rest, hotel, hours):
    # get travel details
    tid = hours[1] - hours[0]
    avg_travel_time = np.mean(distances)/40
    tpr = 1
    tpa = (tid - tpr*num_rest - (num_attr+num_rest-1)*avg_travel_time)/num_attr
    temp_schedule = []
    temp_time = []
    time = hours[0]
    # get top attractions for the day
    idx = attraction_popping(scores, attractions, num_attr, num_rest)
    top_k_attr_rest_idx = [attractions[i] for i in idx]
    attr_and_rest = top_k_attr_rest_idx.copy()
    # calculate distance from hotel
    hotel_to_attraction = [abs((hotel.lat-a.lat))+abs((hotel.lon-a.lon)) for a in top_k_attr_rest_idx]
    hotel_to_attraction_sorted = np.array(hotel_to_attraction).argsort()
    # determine the first attraction
    is_restaurant = False
    if num_rest == 3:
        is_restaurant = True
        time += tpr
    else:
        time += tpa

    for a in hotel_to_attraction_sorted:
        if top_k_attr_rest_idx[a].is_restaurant == is_restaurant:
            closest_attraction = attr_and_rest.pop(a)
            closest_attraction_travel_dist = hotel_to_attraction[a]
            closest_attraction_travel_time = closest_attraction_travel_dist/40
            temp_schedule.append(closest_attraction)
            temp_time.append(closest_attraction_travel_time)
            time += closest_attraction_travel_time
            break
    # greedly select the rest of the attractions
    num_rest_left = num_rest
    while len(attr_and_rest) != 0:
        curr_loc = temp_schedule[-1]
        curr_loc_idx = top_k_attr_rest_idx.index(curr_loc)
        distance_to_others = distances[curr_loc_idx]
        next_location = None
        next_dist = 0
        if (time > 12 and num_rest_left == 2) or (time > 17 and num_rest_left == 1):
            next_location, attr_and_rest, next_dist = next_loc(curr_loc, distance_to_others, attractions, attr_and_rest, True)
            time += tpr
            num_rest_left -= 1
        else:
            next_location, attr_and_rest, next_dist = next_loc(curr_loc, distance_to_others, attractions, attr_and_rest, False)
            time += tpa
        temp_schedule.append(next_location)
        travel_time = next_dist/40
        temp_time.append(travel_time)
        time += travel_time
    # add time back to hotel
    travel_time = hotel_to_attraction[top_k_attr_rest_idx.index(temp_schedule[-1])]/40
    temp_time.append(travel_time)
    time += travel_time
    # calculate attraction scaling factor
    scale = (tid - sum(temp_time))/(tpr*num_rest+tpa*num_attr)
    tpa *= scale
    tpr *= scale
    compile_schedule = compile(temp_time, temp_schedule)
    return compile_schedule, tpa, tpr


#####################################################################
# Main Function
#####################################################################
def main():
    # TODO: |places| < |days|
    # generate synthetic datasets
    synthetic_params = [(35, (0,-10), (5,6)), (33, (12,8), (7,7))]
    random.seed(123)
    attraction_list = gen_syn_loc(synthetic_params, 0.1)

    # clustering configurations
    num_days = 2
    # topk configurations
    hours = (8,21)
    have_breakfast = False
    k_attractions = 5 # TODO: grab this from the maps API/ database
    k_restaurants = 3 if have_breakfast else 2 # TODO: grab this from the maps API/ database
    # filtering configurations
    num_iter = 5000
    neighborhood_frac = 1.5
    bias = 10
    random_max = 5
    random_min = 1
    decay = 5e-2
    hyperparameters = Hyperparameters(num_iter, neighborhood_frac, bias, random_max, random_min, decay)

    L = get_dists(attraction_list)
    l_avg = np.mean(L)
    # curate the score list of each cluster
    S = filter_attraction_list(attraction_list, L, l_avg, k_attractions, k_restaurants, hyperparameters)

    compile_schedule, tpa, tpr = scheduler(S, L, attraction_list, k_attractions, k_restaurants, attraction_list[0], hours)
    print(compile_schedule)
    print("tpa: " + str(tpa))
    print("tpr: " + str(tpr))
    travel_time = 0
    for events in compile_schedule:
        if isinstance(events, (int, float)):
            travel_time += events
    print("Time in the day to do things: " + str(hours[1]-hours[0]))
    print("Time taken: " + str(tpa*k_attractions + tpr*k_restaurants + travel_time))

if __name__ == '__main__':
    main()
