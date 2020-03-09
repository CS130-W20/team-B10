from django.shortcuts import render
import json
from .display_utils import format_schedule
from collections import namedtuple
Attraction = namedtuple('Attraction', ['places_id','lat','lon', 'score', 'is_restaurant'])
attr_info = namedtuple('attr_info', ['name','location'])

def home(request):
    return render(request, 'maps/home.html')

def maps(request):
    return render(request, 'maps/maps.html')

def survey(request):
    return render(request, 'maps/survey.html')

def display(request):

#     dest_and_dates = json.loads(request.GET['dest_and_dates'])
#     survey_result = json.loads(request.GET['survey_result'])
    #convert(start_date, end_date, schedule, tpa, tpr, hotel_name, wake, sleep, num_days)
    sample = [[0.4057137091336608, Attraction(places_id='asdf', lat=-2.180228205246836, lon=-4.001666389604681, score=9.053986522844989, is_restaurant=False), 0.618172714241416, Attraction(places_id='asdf', lat=-2.0089966827975267, lon=-4.454155118915776, score=7.692790899139238, is_restaurant=False), 0.18392860891624427, Attraction(places_id='asdf', lat=0.008785250829872604, lon=-9.653201360155721, score=4.362757934152183, is_restaurant=True), 0.6726163323730452, Attraction(places_id='asdf', lat=-4.136568449219548, lon=-3.0182693918292927, score=9.696860772658779, is_restaurant=False), 0.593984777603214, Attraction(places_id='asdf', lat=0.08295751400808903, lon=-13.795694847641734, score=8.201901844338309, is_restaurant=False), 0.7666097393775685, Attraction(places_id='asdf', lat=-4.377386483269133, lon=-11.215880617868779, score=8.520866189293686, is_restaurant=True), 0.2900272346606112, Attraction(places_id='asdf', lat=-7.857630136177638, lon=-11.921656543232203, score=9.091532756367794, is_restaurant=False), 0.7456485112476189]]
    attractions = {'a': attr_info('a', 'westwood'), 'b': attr_info('b', 'westwood'), 'c': attr_info('c', 'westwood'), 'd': attr_info('d', 'westwood'), 'e': attr_info('e', 'westwood'), 'f': attr_info('f', 'westwood'), 'g': attr_info('g', 'westwood'), 'h': attr_info('h', 'westwood'), 'i': attr_info('i', 'westwood'), 'j': attr_info('j', 'westwood'), 'k': attr_info('k', 'westwood'), 'asdf': attr_info('asdf', 'westwood')}
    tpa = 0.8560141740383967
    tpr = 0.5500776977191706
    events_list = format_schedule("2020-03-08", "2020-03-10", attractions, sample, tpa, tpr, "Budapest", "08:00:00", "23:00:00")
    return render(request, 'maps/display.html', {'itinerary_in_json': json.dumps(events_list)})

def about(request):
    return render(request, 'maps/about.html', {'title': 'About'})
