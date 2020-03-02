from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=200)
    startDate = models.DateField()
    endDate = models.DateField()

class Hotel(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    date = models.DateField()
    place_id = models.CharField(max_length=100)

class Day(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    date = models.DateField()

class Events(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    startTime = models.TimeField()
    endTime = models.TimeField()
    place_id = models.CharField(max_length=100)

class Location(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    icon = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    photo_height = models.IntegerField()
    photo_width = models.IntegerField()
    photo_reference = models.CharField(max_length=100)
    photo_attributions = models.CharField(max_length=200)
    place_id = models.CharField(max_length=100, primary_key=True)
    rating = models.FloatField()
    type_of = models.CharField(max_length=50)
    formatted_address = models.CharField(max_length=200)
    creation_date = models.DateField(auto_now_add=True)