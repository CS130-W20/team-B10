from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='site-home'),
    path('survey/', views.survey, name='site-survey'),
    path('display/', views.display, name='site-display'),
    path('maps/', views.maps, name='site-maps'),
    path('about/', views.about, name='site-about'),
]
