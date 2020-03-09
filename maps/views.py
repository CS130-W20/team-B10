from django.shortcuts import render
import json

def home(request):
    return render(request, 'maps/home.html')

def maps(request):
    return render(request, 'maps/maps.html')

def survey(request):
    return render(request, 'maps/survey.html')

def display(request):
    events_list = []
    event1 = {'title': 'Testing', 'start':'2020-03-14T11:00:00', 'start':'2020-03-14T12:00:00'}
    event2 = {'title': 'Test2', 'start':'2020-03-16T11:00:00', 'start':'2020-03-16T12:00:00'}
    events_list.append(event1)
    events_list.append(event2)
    return render(request, 'maps/display.html', {'itinerary_in_json': json.dumps(events_list)})

def about(request):
    return render(request, 'maps/about.html', {'title': 'About'})
