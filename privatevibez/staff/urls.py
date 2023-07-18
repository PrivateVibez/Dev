
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="staff_home"),
    path('idStatus/', views.Id_Status, name="Id_Status"),
    path('AddDevProject/', views.Add_Dev_Project, name="Add_Dev_Project"),
    path('AddDevList/', views.Add_Dev_List, name="Add_Dev_List"),
]
