from django.urls import path
from . import views
urlpatterns = [
    # urls for logging in, logging out and registration of user
    path('logout', views.Logout, name="logout"),
    path('login/', views.Login, name="login"),
    path('signup/', views.Registration, name="Registration"),
    
    # registration for broadcasters
    path('registration_broadcaster/', views.Registration_Broadcaster, name="registration_broadcaster"),
    path('saveBroacasterInfo/', views.Registration_Broadcaster_info, name="save_broacaster_info"),
    path('saveBroacasterId/', views.Registration_Broadcaster_ID, name="save_broacaster_id"),
    
    # reporting of bad acters
    path('Bad_Acters_Add/', views.Bad_Acters_Add, name="Bad_Acters_Add"),
    
    # urls for sending and buying vibez
    path('Send_Vibez/', views.Send_Vibez, name="Send_Vibez"),
    path('Buy_Vibez/', views.Buy_Vibez, name="Buy_Vibez"),
    
    # url for saving broadcaster profile picture and personal information
    path('Profile_Pic/', views.Profile_Pic, name="Profile_Pic"),
    path('bio_info/', views.bio_info, name="bio_info"),
    
    # url for getting user IP address
    path('get_IP_Address/', views.get_IP_Address, name="get_IP_Address"),
    
    # url for getting total reports
    path('getTotalReports/', views.getTotalReports, name="getTotalReports"),
    
    #url for searching broadcaster and broadcaster TABS i.e. FEATURED, WOMEN, MEN etc.
    path('tabbroadcaster/', views.get_broadcaster, name="tabbroadcaster"),

     #update password
     path('changepassword/', views.changepassword, name="changepassword"),
     
         #  updating email
     path('change_email/', views.change_email, name="change_email"),

]
