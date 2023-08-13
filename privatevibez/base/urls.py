
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="Main_home"),
    path('searchbroadcaster/', views.searchbroadcaster, name="searchbroadcaster"),
    
]
