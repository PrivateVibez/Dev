from django.urls import path
from .views import fan_list, staff_list

from . import views
urlpatterns = [
    path('fan_list/<str:broc>/', fan_list, name='fan_list'),
    path('staff_list/<str:broc>/', staff_list, name='staff_list'),

]