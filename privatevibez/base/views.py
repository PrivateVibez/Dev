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
from django.contrib.sessions.models import Session
from accounts.serializers import User_DataSerializer, Room_DataSerializer,UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
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
          


def room_data_func(request,user_country,user_region):
        
        users = User.objects.filter(Status="Broadcaster")
                
        broadcaster_data = []
        for user in users:
                user_data_list = User_Data.objects.filter(User=user)
                room_data_list = Room_Data.objects.filter(User=user)
                
                for user_data in user_data_list:
                        
                        broadcaster_data.append({
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
                                
                if request.user.is_authenticated:
                        if Bad_Acters.objects.filter(Reporty = request.user.id).exists():
                                blocked_broadcasters = Bad_Acters.objects.filter(Reporty = request.user.id)
                                for blocked_broadcaster in blocked_broadcasters:
                            
                                        if blocked_broadcaster.Reported.id == room.User_id:
                                                rooms_list.append(room.User.id)
                                                
                if is_blocked or is_blocked_region:
                        rooms_list.append(room.User.id) # Append room if user's country is not blocked

                
        for room in rooms_list:
                if any(item["user_id"] == room for item in broadcaster_data):
                        broadcaster_data = [item for item in broadcaster_data if item["user_id"] != room]
                
                                   
                                

        return broadcaster_data if broadcaster_data else None



def home(request):
        
        items_per_page = 4  # Number of items per page
        page_number = request.GET.get('page', 1) 
        if request.user.is_authenticated:
                blocked_broadcasters = Bad_Acters.objects.filter(Reporty = request.user.id)
                try:
                        user_datas        = User_Data.objects.get(User =  request.user)

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
                        
                        
                        broadcaster_data = room_data_func(request,user_status_data.Country,user_status_data.Region)
                        broadcaster_data = paginate_list(page_number, broadcaster_data, items_per_page)

                        
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
                                        broadcaster_data = room_data_func(request,guest_country,guest_region)
                
                                        
                                        broadcaster_data = paginate_list(page_number, broadcaster_data, items_per_page)
                                
                        else:
                                broadcaster_data = room_data_func(request,guest_country,guest_region)
                                broadcaster_data = paginate_list(page_number, broadcaster_data, items_per_page)
                        
                        
                                print(broadcaster_data,flush=True)
                                
                                


        return render(request, "base/home.html", locals())

def paginate_list(page_number, user_data_list, items_per_page):
    
    paginator = Paginator(user_data_list, items_per_page)
    
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    
    return page

def searchbroadcaster(request):
        items_per_page = 4  # Number of items per page
        page_number = request.GET.get('page', 1) 
        if request.method == "GET":

                search = request.GET.get('search')
                if search is not None:
                        
                        broadcasters = Room_Data.objects.filter(
                        Q(hashtags__icontains=search) |
                        Q(User__username__icontains=search)
                        ).filter(User__Status="Broadcaster")
                        
                        print(broadcasters,flush=True)
                        if broadcasters.exists():
                                
                                if request.user.is_authenticated:
                                        user = request.user
                                        user_country = user.Country
                                        user_region = user.Region
                                        
                                        user_ids = broadcasters.values_list('User__id', flat=True)
                                        users = User.objects.filter(id__in=user_ids)    
                                                                                    
                                        broadcaster_data = []
                                        for user in users:
                                                
                                                user_data_list = User_Data.objects.filter(User=user)
                                                room_data_list = Room_Data.objects.filter(User=user)
                                                
                                                for user_data in user_data_list:
                                                        
                                                        broadcaster_data.append({
                                                                                        "user_id": user.id,
                                                                                        "username": user.username,
                                                                                        "Image": user_data.Image.url,
                                                                                        })

                                        
                                        rooms_list = []
                                        
                                        for broadcaster in broadcasters:
                                                                                
                                                country_blocked = False
                                                region_blocked = False
                                                for blocked_country in broadcaster.Blocked_Countries.all():
                                                        if blocked_country.Country.code2 == user_country:
                                                                country_blocked = True
                                                                break  # If the user's country is blocked, no need to check other blocked countries
                                                
                                                for blocked_region in broadcaster.Blocked_Regions.all():
                                                        if blocked_region.Region.display_name == user_region:
                                                                region_blocked = True
                                                                break
                                                if country_blocked or region_blocked:
                                                        rooms_list.append(broadcaster.User.id)
                                                        
                                                print(rooms_list,flush=True)        
                                                for room in rooms_list:
                                        
                                                        if any(item["user_id"] == room for item in broadcaster_data):
                                                                broadcaster_data = [item for item in broadcaster_data if item["user_id"] != room]
                                                                
                                                                
                                                if Bad_Acters.objects.filter(Reporty = request.user.id).exists():
                                                        print(request.user.id,flush=True)
                                                        blocked_broadcasters = Bad_Acters.objects.filter(Reporty = request.user.id)
                                                        for blocked_broadcaster in blocked_broadcasters:
                                                                
                                                                if any(item["user_id"]  == blocked_broadcaster.Reported.id for item in broadcaster_data):
                                                                        
                                                                        broadcaster_data = [item for item in broadcaster_data if item["user_id"] != blocked_broadcaster.Reported.id]
                                                                                
                                        
                                        return render(request, "base/home.html", locals())                                      
                                else:
                                        
                                        broadcaster_data = []
                                        guest_country = request.session.get('guest_country')
                                        guest_region = request.session.get('guest_region')
                                        
                                        user_ids = broadcasters.values_list('User__id', flat=True)
                                        users = User.objects.filter(id__in=user_ids)    
                                                                                    
                                        broadcaster_data = []
                                        for user in users:
                                                user_data_list = User_Data.objects.filter(User=user)
                                                room_data_list = Room_Data.objects.filter(User=user)
                                                
                                                for user_data in user_data_list:
                                                        
                                                        broadcaster_data.append({
                                                                                        "user_id": user.id,
                                                                                        "username": user.username,
                                                                                        "Image": user_data.Image.url,
                                                                                        })

                                      
                                        rooms_list = []

                                        for room in broadcasters:
                                                is_blocked = False  # Initialize a flag to indicate if user's country is 
                                                is_blocked_region = False #
                                                for blocked_country in room.Blocked_Countries.all():
                                                        country = blocked_country.Country.code2
                                                        if country == guest_country:
                                                                is_blocked = True  # Set the flag if user's country is blocked
                                                                
                                                                break 
                                                for blocked_regions in room.Blocked_Regions.all():
                                                        region = blocked_regions.Region.display_name
                                                        if region == guest_region:
                                                                is_blocked = True
                                                                
                                                if is_blocked or is_blocked_region:
                                                        rooms_list.append(room.User.id) # Append room if user's country is not blocked

                                        
                                        for room in rooms_list:
                                        
                                                if any(item["user_id"] == room for item in broadcaster_data):
                                                        broadcaster_data = [item for item in broadcaster_data if item["user_id"] != room]
                                                
                                                
                                        # Store broadcaster data in a session
                                        request.session['user_data_list'] = broadcaster_data 
                                                   
                                        broadcaster_data = paginate_list(page_number, broadcaster_data, items_per_page)
                

                                
                                
                                print(broadcaster_data,flush=True)
                                return render(request, "base/home.html", locals())  

                        else:
                                
                                return render(request, "base/home.html", {"no_broadcaster_found": True})  
                else:
                        if page_number is not None:
                                # get the stored broadcaster data
                                broadcaster_data = request.session.get('user_data_list')
                                broadcaster_data = paginate_list(page_number, broadcaster_data, items_per_page)
                                return render(request, "base/home.html", locals())  
                        print("request is not get",flush=True)


