from django.urls import path
from . import views
urlpatterns = [
    path('logout', views.Logout, name="logout"),
    path('login/', views.Login, name="login"),
    path('signup/', views.Registration, name="Registration"),
    path('registration_broadcaster/', views.Registration_Broadcaster, name="registration_broadcaster"),
    path('saveBroacasterInfo/', views.Registration_Broadcaster_info, name="save_broacaster_info"),
    path('saveBroacasterId/', views.Registration_Broadcaster_ID, name="save_broacaster_id"),
    path('Bad_Acters_Add/', views.Bad_Acters_Add, name="Bad_Acters_Add"),
    path('Send_Vibez/', views.Send_Vibez, name="Send_Vibez"),
    path('Buy_Vibez/', views.Buy_Vibez, name="Buy_Vibez"),
    path('Profile_Pic/', views.Profile_Pic, name="Profile_Pic"),
    path('bio_info/', views.bio_info, name="bio_info"),



]
