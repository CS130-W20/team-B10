from django.shortcuts import render
import json

def home(request):
    return render(request, 'maps/home.html')

def maps(request):
    return render(request, 'maps/maps.html')

def survey(request):
    return render(request, 'maps/survey.html')

def display(request):
    dest_and_dates = json.loads(request.GET['dest_and_dates'])
    survey_result = json.loads(request.GET['survey_result'])
    return render(request, 'maps/display.html')

def about(request):
    return render(request, 'maps/about.html', {'title': 'About'})
