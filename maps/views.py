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
    #convert(start_date, end_date, schedule, tpa, tpr, hotel_name, wake, sleep, num_days)
    sample = [[0.29140672058361233, Attraction(places_id='a', lat=3.321948489954936, lon=-4.931563542804515, score=7.761329698240371, is_restaurant=False), 0.14609907173092168, Attraction(places_id='b', lat=2.311880741996689, lon=-8.17104514814322, score=7.9007184435880164, is_restaurant=False), 0.49313966786740604, Attraction(places_id='c', lat=24.674806223650624, lon=14.800595944918582, score=0.5715921340929664, is_restaurant=False), 0.4057137091336608, Attraction(places_id='d', lat=-2.180228205246836, lon=-4.001666389604681, score=9.053986522844989, is_restaurant=False), 0.26451075434659305, Attraction(places_id='e', lat=-4.377386483269133, lon=-11.215880617868779, score=8.520866189293686, is_restaurant=True), 0.07915230824922867, Attraction(places_id='f', lat=-1.9042933758845186, lon=-10.522881395284246, score=6.942059146992349, is_restaurant=False), 0.0, Attraction(places_id='g', lat=-2.0089966827975267, lon=-4.454155118915776, score=7.692790899139238, is_restaurant=False), 0.5556490078753418, Attraction(places_id='h', lat=-4.136568449219548, lon=-3.0182693918292927, score=9.696860772658779, is_restaurant=False), 0.7994123525394244, Attraction(places_id='i', lat=0.08295751400808903, lon=-13.795694847641734, score=8.201901844338309, is_restaurant=False), 0.48066624524480445, Attraction(places_id='j', lat=0.008785250829872604, lon=-9.653201360155721, score=4.362757934152183, is_restaurant=True), 0.8876094811216774, Attraction(places_id='k', lat=-4.74147523734855, lon=-14.641275291754532, score=8.093385246438048, is_restaurant=False), 0.4421032064161491, Attraction(places_id='l', lat=-7.857630136177638, lon=-11.921656543232203, score=9.091532756367794, is_restaurant=False), 0.7456485112476189]]
    attractions = {'a': attr_info('disney', 'anaheim'), 'b': attr_info('chick-fil-a', 'westwood'), 'c': attr_info('chick-fil-a', 'westwood'), 'd': attr_info('chick-fil-a', 'westwood'), 'e': attr_info('chick-fil-a', 'westwood'), 'f': attr_info('chick-fil-a', 'westwood'), 'g': attr_info('chick-fil-a', 'westwood'), 'h': attr_info('chick-fil-a', 'westwood'), 'i': attr_info('chick-fil-a', 'westwood'), 'j': attr_info('chick-fil-a', 'westwood'), 'k': attr_info('chick-fil-a', 'westwood'), 'l': attr_info('chick-fil-a', 'westwood')}
    tpa = 1.3339635511830208
    tpr = 1.8792927708532825
    events_list = format_schedule("2020-03-08", "2020-03-10", attractions, sample, tpa, tpr, "Budapest", "08:00:00", "23:00:00")
    return render(request, 'maps/display.html', {'itinerary_in_json': json.dumps(events_list)})

def about(request):
    return render(request, 'maps/about.html', {'title': 'About'})
