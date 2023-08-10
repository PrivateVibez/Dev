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
                                        if key == "lat":
                                                user_status_data.latitude = value
                                                user_status_data.save()
                                        if key == "lng":
                                                user_status_data.longitude = value
                                                user_status_data.save()
                
        else:
                print("Request failed with status code:", response.status_code)



def get_guest_location(request,ip_address):
        
        url = "https://geo.ipify.org/api/v2/country,city"
        
        data = {
                "apiKey":"at_HxIk3g73CVFEeZN2rAAsT7a81ROxs",
                "ipAddress": ip_address,
        }
        
        response = requests.get(url, params=data)
        
        if response.status_code == 200:
                json_data = response.json()
                for key, value in json_data.items():
                        if key == "location":
                                for key, value in value.items():
                                        if key == "country":
                                                country = value
                                                request.session['guest_country'] = country
                                        if key == "region":
                                                region = value
                                                request.session['guest_region'] = region
          


def room_data_func(user_country,user_region):
        users = User.objects.filter(Status="Broadcaster")       
        combined_fields_list = []
        for user in users:
                user_data_list = User_Data.objects.filter(User=user)
                room_data_list = Room_Data.objects.filter(User=user)
                
                for user_data in user_data_list:
                        
                        combined_fields_list.append({
                                                        "user_id": user.id,
                                                        "username": user.username,
                                                        "Image": user_data.Image.url,
                                                        })

        rooms = Room_Data.objects.filter(User__Status="Broadcaster")
        rooms_list = []

        for room in rooms:
                is_blocked = False  # Initialize a flag to indicate if user's country is 
                is_blocked_region = False #
                for blocked_country in room.Blocked_Countries.all():
                        country = blocked_country.Country.code2
                        if country == user_country:
                                is_blocked = True  # Set the flag if user's country is blocked
                                
                                break 
                for blocked_regions in room.Blocked_Regions.all():
                        region = blocked_regions.Region.display_name
                        if region == user_region:
                                is_blocked = True
                                
                if is_blocked or is_blocked_region:
                        rooms_list.append(room.User.id) # Append room if user's country is not blocked

        
        for room in rooms_list:
            
                if any(item["user_id"] == room for item in combined_fields_list):
                        combined_fields_list = [item for item in combined_fields_list if item["user_id"] != room]
                        
        return combined_fields_list



def home(request):

        if request.user.is_authenticated:
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
                        
                        
                        combined_fields_list = room_data_func(user_status_data.Country,user_status_data.Region)
                        
                        
                except(User_Status.DoesNotExist, User_Data.DoesNotExist):
                        if StaffManager.objects.filter(staff_id_id = request.user).exists():
                                return redirect('staff/')
        else:
                if request.user.is_anonymous:
                        guest_ip = request.session.get('ip_address')
                        guest_country = request.session.get('guest_country')
                        guest_region = request.session.get('guest_region')
                        
                        if guest_ip is None and guest_country is None:
                                url = "https://api.ipify.org?format=text"
                                response = requests.get(url)
                                if response.status_code == 200:
                                        request.session['ip_address'] = response.text
                                        guest_ip = request.session.get('ip_address')
                                        get_guest_location(request,guest_ip)
                                        guest_country = request.session.get('guest_country')
                                        guest_region = request.session.get('guest_region')
                                        combined_fields_list = room_data_func(guest_country,guest_region)
                                        
                                        
                                        # rooms_list = Room_Data.objects.filter( User__Status="Broadcaster")
                                        # room_users_data = User_Data.objects.filter( User__Status="Broadcaster")
                        else:
                                combined_fields_list = room_data_func(guest_country,guest_region)
                                print(combined_fields_list,flush=True)


        return render(request, "base/home.html", locals())




