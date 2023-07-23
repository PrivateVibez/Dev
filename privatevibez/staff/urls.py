
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="staff_home"),
    path('idStatus/', views.Id_Status, name="Id_Status"),
    path('createStaff/', views.Create_Staff, name="Create_Staff"),
    path('editStaffPermission/', views.editStaffPermission, name="editStaffPermission"),
    path('sendStaffInvitation/', views.sendStaffInvitation, name="sendStaffInvitation"),
    path('staffRegistration/', views.staffRegistration, name="staffRegistration"),
    path('AddDevProject/', views.Add_Dev_Project, name="Add_Dev_Project"),
    path('AddDevList/', views.Add_Dev_List, name="Add_Dev_List"),
    path('getPermission/', views.getPermission, name="getPermission"),
    path('getStaffInformation/', views.getStaffInformation, name="getStaffInformation"),
]
