from django.shortcuts import render
from accounts.models import *
from rooms.models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib import messages
from staff.models import StaffManager
from django.shortcuts import redirect
import requests
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

def get_IpAddress():
        
        url = "https://api.ipify.org?format=text"
        ip = requests.get(url).text
        
        return ip

def get_Location(user_status_data,ip_address):
        url = "https://geo.ipify.org/api/v2/country,city"
        
        data = {
                "apiKey":"at_HxIk3g73CVFEeZN2rAAsT7a81ROxs",
                "ipAddress": ip_address,
        }
        
        response = requests.get(url, params=data)
        
        if response.status_code == 200:
                json_data = response.json()
                user_status_data.Ip_Address = ip_address
                user_status_data.Ip_Address_Expires = timezone.now() + timedelta(days=7)
                user_status_data.save()
                for key, value in json_data.items():
                        if key == "location":
                                for key, value in value.items():
                                        if key == "country":
                                                user_status_data.Country = value
                                                user_status_data.save()
                                        if key == "region":
                                                user_status_data.Region = value
                                                user_status_data.save()
                
        else:
                print("Request failed with status code:", response.status_code)

def home(request):

        if request.user.is_authenticated :
                blocked_broadcasters = Bad_Acters.objects.filter(Reporty = request.user.id)
                try:
                        
                        user_status_data = User.objects.get(id = request.user.id)
                        user_status      = user_status_data.Status
                        
                        if user_status_data.Ip_Address is None:
                                ip_address = get_IpAddress()
                                get_Location(user_status_data,ip_address)
                        else:
                                if user_status_data.Ip_Address_Expires <= timezone.now():
                                        user_status_data.Ip_Address_Expires = timezone.now() + timedelta(days=7)
                                        ip_address = get_IpAddress()
                                        get_Location(user_status_data,ip_address)
 
                        
                        if user_status_data.Country is None:
                                pass
                        
                        rooms = Room_Data.objects.filter( User__Status="Broadcaster")
                        rooms_list = []
                        user_data = User_Data.objects.filter(User__in=[data.User for data in rooms])
                       
                        for room in rooms:
                                is_blocked = False  # Initialize a flag to indicate if user's country is blocked
                                for blocked_country in room.Blocked_Countries.all():
                                        country = blocked_country.Country.code2
                                        if country == user_status_data.Country:
                                                is_blocked = True  # Set the flag if user's country is blocked
                                                break  # No need to check other blocked countries once blocked is found
                                if not is_blocked:
                                        rooms_list.append(room)  # Append room if user's country is not blocked


                        print('s')    
                        print(rooms_list)
                except(User_Status.DoesNotExist, User_Data.DoesNotExist):
                        if StaffManager.objects.filter(staff_id_id = request.user).exists():
                                return redirect('staff/')
        else:
        #         room_users_data = User_Data.objects.all()
                pass
                
        
        # rooms_list = Room_Data.objects.filter( User__Status="Broadcaster")

        # room_users_data = User_Data.objects.filter( User__Status="Broadcaster")

                


        return render(request, "base/home.html", locals())




