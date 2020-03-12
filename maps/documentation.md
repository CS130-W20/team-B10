# Python Functions API Documentation

## filter_scores.py
```python
get_cluster_id_list(xys_list, num_clusters):
Forms a specified number of clusters from a given list of coordinate and score tuples using k-means.
Args:
xys_list (list): list of tuples containing the x coordinate, y 
coordinate, and score
num_clusters (int): the number of clusters for k-means to form
Returns:
cluster_id_list (list): list of cluster labels corresponding to the 
coordinate list
centroids (list): list of centroids returned by k-means
 
cluster_xys_list(cluster_id_list, xys_list, num_clusters):
Separates the coordinate list by their respective clusters.    
Args:
cluster_id_list (list): list of cluster labels corresponding to the 
coordinate list
xys_list (list): list of tuples containing the x coordinate, y 
coordinate, and score
num_clusters (int): number of clusters formed by k-means   
Returns:
xys_list_clusters (list): list of coordinate list separated by 
their clusters
 
filter_xys_list(xys_list, max_itr, num_neighbors, sensitivity, bias):
Refines the xys_list scores and filters the list, resulting in a xys_list 
containing num_neighbors highest score
Args:
xys_list (list): list of tuples containing the x coordinate, y 
coordinate, and score
max_itr (int): maximum number of score refinement interations
num_neighbors (int): the number of locations to keep for each 
Cluster
sensitivity (int): sensitivity
bias (int): bias
    Returns:
xys_filtered_list (list): filtered list of num_neighbor highest
scoring coordinates
 
get_dists(xys_list):
Gets the l2 distance between all coordinate pairs 
Args:
xys_list (list): list of tuples containing the x coordinate, y 
coordinate, and score
Returns:
L (list): 2d list of l2 distances between each pair of coordinates

plot(xys_list, ax, k=None):
Plots the coordinates based on their cluster labels
Args:
xys_list (list): list of tuples containing the x coordinate, y 
coordinate, and score
ax: matplot graph object
 		k (int): number of clusters (number of days)
Returns:
Generates a graph containing the coordinates and labels
```
## schedule.py
```python
attraction_popping(scores, attractions, num_attr, num_rest):
Sorts attractions by scores
Args: 
scores (list): list of attraction scores
attractions (list): list of atttractions
num_attr (int): the number of attractions to visit each day
num_rest (int): the number of restaurants to visit each day
Returns:
top_k_attr_rest_idx (list): a list of the index of the top k attractions

next_loc(attr, distance, attrs, new_top_k_attr, is_rest):
Given an attraction, finds the closest next attraction
Args:
attr (Attraction): a single Attraction(places_id, lat, lon, score, is_restaurant)
distance (list): a list of distances between attractions
attrs (list): a list of Attractions
new_top_k_attr (list): top k attractions sorted by score
is_rest (bool): if the attraction is a restaurante
Returns:
attraction (Attraction): the next attraction to go to
new_top_k_attr (list): top k attractions with the next attraction popped
distance[attr.index(attraction)] (float): distance from current to the next attraction

compile(time, attraction):
Compiles the attractions and travel time in to one list
Args:
time (list): list of floats that specify the travel time between attractions
attraction (list): list of attractions to be scheduled
Returns:
final (list): list of attractions scheduled

scheduler(scores, distances, attractions, num_attr, num_rest, hotel, hours):
Creates the actual schedule using the scores and distances between attractions. Also calcuates the time of travel between each attraction.
Args:
scores (list): list of the scores of each attraction
distance (list): list of the distances between each attraction
num_attr (int): number of attractions to visit each day
num_rest (int): number of restaurants to visit each day
hotel (Attraction): the named Attraction tuple, containing hotel information
hours (list): a list containing the time to start the day and time to end the day
```

## display_utils.py
```python
days_between(d1, d2):
Calculates the number of days between the two dates
Args:
d1 (datetime): a datetime object corresponding to the start date
d2 (datetime): a datetime object corresponding to the end date
Returns:
(int): an int corresponding to the number of days between the start and end date

time_string_to_decimals(time_string):
Converts a time string to a decimal
Args:
time_string (string): a time string (HH:MM:SS)
Returns:
(float): a float corrsponding to the converted time string

attr_to_tup(attrs, is_rest=False):
Converts a list of attractrions returned by the Google places API to a list of named Attraction tuples.
Args:
attrs (list): list of attractrions returned by the Google places API
is_rest (bool): indicates whether the attraction is a restaurant or not
Returns:
attr_tup (list): list of named tuples called Attractions containing attraction id, lat, lon, and rating

clustering(num_days, have_breakfast, k_attractions, attraction_list):
Generates the clusters based on the number of days.
Args:
num_days (int): the number of days (clusters)
have_breakfast (bool): personalization survey result indicated whether to schedule breakfast or not
k_attractions (int): how many attractions to schedule for each day
k_restaurants (int): how many restaurants to schedule for each day
attraction_list (int): list of the attractions to cluster

scheduling(attraction_list_clusters, k_attractions, k_restaurants, hotel, hours):
Generates a schedule given attraction clusters.
Args:
attraction_list_clusters (list): a list of attraction clusters, where each cluster is a list of attractions
k_attractions (int): how many attractions to schedule for each day
k_restaurants (int): how many restaurants to schedule for each day
hotel (Attraction): a Attraction tuple corresponding to a the hotel
hours (list): a list containing the time to start the day and time to end the day
Returns:
schedules (list): a list of tuples which contains the schedule, time per attraction, and time per restaurant.

format_schedule(start_date, end_date, placeid_dict, schedule_list, tpa_list, tpr_list, hotel_name, wake, sleep):
Converts a schedule into a list of events to be converted to json to be read by the calendar.
Args:
start_date (string): a string containing the starting date of the trip
end_date (string): a string containing the ending date of the trip
placeid_dict (dict): a dictionary that converts a placeid into the name and location of an attraction
schedule_list (list): a list containing a list of schedules, where each schedule corresponds to each day
tpa_list (list): a list of time per attraction corresponding to each day
tpr_list (list): a list of time per restaurant corresponding to each day
hotel_name (string): the name of the hotel to stay at each night
wake (string): a string (HH:MM:SS) corresponding to the time to start the day
sleep (string): a string (HH:MM:SS) corresponding to the time to end the day
Returns:
events_list (list): a list of events (which is a dictionary) containing the name, start time, end time, and color of the event to be displayed on the calendar

find_hotel(centroids, api, radius):
Finds a hotel to stay at based on the centroid.
Args:
centroid (list): a list representing the centroid of the clusters
api (string): the Google api key to use google places search
radius (int): the radius to conduct the hotel search
Returns:
hotels[0]: the first hotel returned by the google places api

make_dict(attrs):
Given the google places search result, creates a dictionary that converts the placeid to the name and location of the result.
attrs (list): the google places search result, containing a list of possible attractions and its data.
Returns:
place_id (dict): dictionary with the placeid as the key, and the name and location of the attraction as the value.
```

## placesapi.py
```python
search_places(location, radius, type, api):
Obtain list of nearby locations of a certain type
Args:
location (string): string of latitude and longitude
radius (int): radius in meters from provided location in which to search
type (string): the type of location
api (string): the API key
Returns:
Places (list): list of nearby places
```