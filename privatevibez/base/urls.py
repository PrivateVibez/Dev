
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="Main_home"),
    
    # url for searching broadcaster
    path('searchbroadcaster/', views.searchbroadcaster, name="searchbroadcaster"),
    
]
