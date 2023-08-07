from django.shortcuts import render
from django.contrib.auth.models import User
from rooms.models import *
from accounts.models import *
from chat.models import *
from cities_light.models import Country, Region, City
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from django.utils.safestring import mark_safe
import json
from .forms import Slot_MachineForm, Fav_vibezForm
from django.http import HttpResponse as httpresponse
import requests
from cryptography.fernet import Fernet
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .serializers import Private_Chat_InviteeSerializer
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def Room(request, Broadcaster):

    if request.user.is_authenticated:
             
            user_data        = User_Data.objects.get(User =  request.user)
            user_status_data = User.objects.get(id = request.user.id)
            user_status      = user_status_data.Status
            broadcaster_user     = User.objects.get(username = Broadcaster)
            room_name_json       = mark_safe(json.dumps(broadcaster_user.username))
            room_name            = broadcaster_user.username
            username             = mark_safe(json.dumps(request.user.username))
            rooms                = Room_Data.objects.all()
            room_users_data      = User_Data.objects.all()    
            broadcaster_status   = User_Status.objects.get(User = User.objects.get(username = Broadcaster))
            room_data            = Room_Data.objects.get(User = User.objects.get(username = Broadcaster))
            # room_sesson          = Room_Sesson.objects.get(User = User.objects.get(username = Broadcaster))
            broadcaster_data     = User_Data.objects.get(User = User.objects.get(username = Broadcaster))

    
        
            private_chat = Private.objects.filter(
                Q(From=request.user, To=broadcaster_user) | Q(To=request.user, From=broadcaster_user)
            ).order_by('Timestamp')

                
            public_chat          = Public.objects.filter(Room = User.objects.get(username=Broadcaster)).all
            follows              = Follows.objects.filter(User = request.user).all()
            
            
            thumbs_up_count      = Thumbs.objects.filter(Broacaster = User.objects.get(username = Broadcaster), Thumb = "Up").count
            thumbs_down_count    = Thumbs.objects.filter(Broacaster = User.objects.get(username = Broadcaster), Thumb = "Down").count
            if Thumbs.objects.filter(User = request.user,Broacaster = User.objects.get(username = Broadcaster),Thumb = "Up").exists():
                thumbs_up_color  = True
            else:
                thumbs_up_color  = False
            if Thumbs.objects.filter(User = request.user,Broacaster = User.objects.get(username = Broadcaster),Thumb = "Down").exists():
                thumbs_Down_color  = True
            else:
                thumbs_Down_color  = False

            if Follows.objects.filter(User = request.user, Broacaster=broadcaster_user.id).exists():
                follow_button = True
            else:
                follow_button = False
                
                
                try:
            
                        private_invitee_list = Private_Chat_Invitee.objects.get(broadcaster = broadcaster_user)
                        private_invitee_list = private_invitee_list.Invitee.all()
                        invitee_list = []
            
                        for user_data in private_invitee_list:
                            if user_data.Is_Accepted_Invite == True:
                                invitee_list.append({
                                    'user_id': user_data.id,
                                    'name': user_data.username,
                                })
                                
                            if user_data.id == request.user.id and user_data.Is_Accepted_Invite == True:
                                invite_accepted = True
                                
                            if user_data.id == request.user.id and user_data.Is_Accepted_Invite == False and user_data.Is_Sent_Invite == True:
                                invite_sent = False
                                
                except Private_Chat_Invitee.DoesNotExist:
                        invitee_list = []
                
            try:
                user =User_Status.objects.get(User = request.user.id)
                
                if user.Status == "User":
                    if Slot_Machine.objects.filter(User=broadcaster_user.id).exists():
                        slot_machine_data = Slot_Machine.objects.filter(User=broadcaster_user.id).values('Slot_cost_per_spin', 'Win_3_of_a_kind_prize', 'Win_2_of_a_kind_prize').get()
                        
                                
                elif user.Status == "Broadcaster":
                    countries = Country.objects.all()
                    room_data_blocked_countries = room_data.Blocked_Countries.all()
                    print(room_data_blocked_countries)
              
                    # Extract a list of blocked country IDs
                    blocked_country_ids = room_data_blocked_countries.values_list('Country_id', flat=True)

                    # Filter countries based on blocked country IDs
                    filtered_countries = countries.exclude(id__in=blocked_country_ids)
                    print(filtered_countries)

                    regions = Region.objects.all()
                    
                    if Slot_Machine.objects.filter(User=request.user).exists():
                        slot_machine_data = Slot_Machine.objects.filter(User=request.user).values('Slot_cost_per_spin', 'Win_3_of_a_kind_prize', 'Win_2_of_a_kind_prize').get()
                
                
            except User_Status.DoesNotExist:
                messages.error(request, 'User does not exist')
    
    else:
        pass
    return render(request, "rooms/home.html", locals())


@csrf_exempt
def Menu_item(request):
    Menu_Data.objects.create(
        User       = request.user,
        Vibez_Cost  =  request.POST.get('Vibez'),
        Menu_Name   = request.POST.get('Menu_Name'),
        Menu_Time   =  request.POST.get('Menu_Time')
    )
    return JsonResponse('OK', safe=False) 

@csrf_exempt
def Dice_items(request):
    if Dice_Data.objects.filter(User = request.user).exists():
        dice_data                   = Dice_Data.objects.get(User = request.user)
        dice_data.One_Dice_Name     =  request.POST.get('1_dice_Name')
        dice_data.One_Dice_Time     =  request.POST.get('1_dice_Time')
        dice_data.Two_Dice_Name     =  request.POST.get('2_dice_Name')
        dice_data.Two_Dice_Time     =  request.POST.get('2_dice_Time')
        dice_data.Three_Dice_Name   =  request.POST.get('3_dice_Name')
        dice_data.Three_Dice_Time   =  request.POST.get('3_dice_Time')
        dice_data.Four_Dice_Name    =  request.POST.get('4_dice_Name')
        dice_data.Four_Dice_Time    =  request.POST.get('4_dice_Time')
        dice_data.Five_Dice_Name    =  request.POST.get('5_dice_Name')
        dice_data.Five_Dice_Time    =  request.POST.get('5_dice_Time')
        dice_data.Six_Dice_Name     =  request.POST.get('6_dice_Name')
        dice_data.Six_Dice_Time     =  request.POST.get('6_dice_Time')
        dice_data.save()
        return JsonResponse('OK', safe=False) 
    else:
        Dice_Data.objects.create(
            User            =  request.user,
            One_Dice_Name   =  request.POST.get('1_dice_Name'),
            One_Dice_Time   =  request.POST.get('1_dice_Time'),
            Two_Dice_Name   =  request.POST.get('2_dice_Name'),
            Two_Dice_Time   =  request.POST.get('2_dice_Time'),
            Three_Dice_Name =  request.POST.get('3_dice_Name'),
            Three_Dice_Time =  request.POST.get('3_dice_Time'),
            Four_Dice_Name  =  request.POST.get('4_dice_Name'),
            Four_Dice_Time  =  request.POST.get('4_dice_Time'),
            Five_Dice_Name  =  request.POST.get('5_dice_Name'),
            Five_Dice_Time  =  request.POST.get('5_dice_Time'),
            Six_Dice_Name   =  request.POST.get('6_dice_Name'),
            Six_Dice_Time   =  request.POST.get('6_dice_Time')
            )
        return JsonResponse('OK', safe=False) 

@csrf_exempt
def Menu_item(request):
    Menu_Data.objects.create(
        User        = request.user,
        Vibez_Cost  = request.POST.get('Vibez'),
        Menu_Name   = request.POST.get('Menu_Name'),
        Menu_Time   = request.POST.get('Menu_Time')
    )
    return JsonResponse('OK', safe=False) 

@csrf_exempt
def Following(request):
    if Follows.objects.filter(User = request.user).exists():
        if Follows.objects.filter(Broacaster = User.objects.get(username = request.POST.get('broadcaster'))).exists():

            Del_flow = Follows.objects.get(User = request.user, Broacaster = User.objects.get(username = request.POST.get('broadcaster')) )
            Del_flow.delete()
        else:
            Follows.objects.create(
                User         =  request.user,
                Broacaster   =   User.objects.get(username = request.POST.get('broadcaster'))
            )
    else:
            Follows.objects.create(
                User         =  request.user,
                Broacaster   =   User.objects.get(username = request.POST.get('broadcaster'))
            )
    return JsonResponse('OK', safe=False) 


def Thumb(request):
    if Thumbs.objects.filter(User = request.user).exists():
        if Thumbs.objects.filter(Broacaster = User.objects.get(username = request.POST.get('broadcaster'))).exists():
            if request.POST.get('Thumb') == "Down":
                thumb = Thumbs.objects.get(User = request.user, Broacaster = User.objects.get(username = request.POST.get('broadcaster')) )
                thumb.Thumb = "Down"
                thumb.save()
            else:
                thumb = Thumbs.objects.get(User = request.user, Broacaster = User.objects.get(username = request.POST.get('broadcaster')) )
                thumb.Thumb = "Up"
                thumb.save()
        else:
            if request.POST.get('Thumb') is "Down":
                Thumbs.objects.create(
                    User         =  request.user,
                    Broacaster   =   User.objects.get(username = request.POST.get('broadcaster')),
                    Thumb        =   "Down"
                )
            else:
                Thumbs.objects.create(
                    User         =  request.user,
                    Broacaster   =   User.objects.get(username = request.POST.get('broadcaster')),
                    Thumb        =   "Up"
                )
    else:
        if request.POST.get('Thumb') is "Down":
            Thumbs.objects.create(
                User         =  request.user,
                Broacaster   =   User.objects.get(username = request.POST.get('broadcaster')),
                Thumb        =   "Down"
            )
        else:
            Thumbs.objects.create(
                User         =  request.user,
                Broacaster   =   User.objects.get(username = request.POST.get('broadcaster')),
                Thumb        =   "Up"
            )
    return JsonResponse('OK', safe=False) 

def PrivateChatCheckBox(request):
    room_data = Room_Data.objects.get(User = request.user)
    room_data.Private_Chat = request.POST.get('Checked')
    room_data.save()
    return JsonResponse('OK', safe=False) 

def Chat(request):
    room_data = Room_Data.objects.get(User = request.user)
    room_data.Public_Chat = request.POST.get('Public_Chat_Check')
    room_data.Private_Chat_Price = int(request.POST.get('PrivateChatPrice'))
    room_data.save()
    return JsonResponse('OK', safe=False) 

def Save_RoomPatterns(request):
    room                       = Room_Data.objects.get(User = request.user)
    room.Price_MMM_button      = request.POST.get('Price_MMM')
    room.Price_OH_button       = request.POST.get('Price_OH')
    room.Price_OHYes_button    = request.POST.get('Price_OHYes')
    room.Duration_MMM_button   = request.POST.get('Duration_MMM')
    room.Duration_OH_button    = request.POST.get('Duration_OH')
    room.Duration_OHYes_button = request.POST.get('Duration_OHYes')
    room.Strength_MMM_button   = request.POST.get('Strength_MMM')
    room.Strength_OH_button    = request.POST.get('Strength_OH')
    room.Strength_OHYes_button = request.POST.get('Strength_OHYes')
    
    room.Feature_OHYes_button = request.POST.get('Feature_OHYes')
    room.Feature_OH_button = request.POST.get('Feature_OH')
    room.Feature_MMM_button = request.POST.get('Feature_MMM')
    
    room.save()
    return JsonResponse('OK', safe=False)


def go_online(request):
    
    if request.method == "POST":
        room_data = Room_Data.objects.get(User = request.user)
        room_data.Is_Active = True
        room_data.save()
        return JsonResponse('OK', safe=False)



def go_offline(request):
    
    if request.method == "POST":
        room_data = Room_Data.objects.get(User = request.user)
        room_data.Is_Active = False
        room_data.save()
        return JsonResponse('OK', safe=False)
    
def block_countries(request):
    
        url = "https://geo.ipify.org/api/v2/country,city"

        data = {
            "apiKey":"at_HxIk3g73CVFEeZN2rAAsT7a81ROxs",
            "ipAddress": "180.190.7.16",
                }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        #response = requests.request("GET", url, headers=headers, params=data)
        
        return JsonResponse(response.json(), safe=False)

    


@csrf_exempt
def set_slot_machine(request):
    
    
    if request.method == "POST":
        form = Slot_MachineForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
            
            return JsonResponse("Saved", safe=False)


@csrf_exempt
def deduct_vibez(request,vibez):
 
    if request.method == "POST":
        user_data = User_Data.objects.get(User_id = request.user)
        user_data.Vibez = user_data.Vibez - vibez
        user_data.save()
       
    
        return JsonResponse("saved", safe=False)
    

@csrf_exempt
def get_prize(request):
    
    if request.method == 'POST':
  
        url = "https://api.lovense-api.com/api/lan/v2/command"
        d_token = settings.LOVENSE_DEV_KEY
        
        utoken = User_Data.objects.get(User = request.user)
        data = {
            "token":d_token,
            "uid": request.user.id,
            "command": "Function",
            "action": request.POST.get('prize_won'),
            "timeSec": float(request.POST.get('duration')),
            "apiVer": 1,
                }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            # Make the POST request using the requests library
            response = requests.post(url, json=data, headers=headers)

            # Check the response status code for success (e.g., 200)
            if response.status_code == 200:
                # Handle the successful response data
                response_data = response.json()
                
        
                owner = Slot_Machine.objects.get(User = request.POST.get('broadcaster'))
                winner = User.objects.get(User = request.POST.get('winner'))
                owner.Winner = winner
                owner.Prize = request.POST.get('prize_won')
                owner.save()
        
 
                
                return JsonResponse(response_data)

            # Handle other status codes if needed
            else:
                return JsonResponse({"error": "Failed to make the POST request."}, status=response.status_code)

        except requests.exceptions.RequestException as e:  
            return JsonResponse({"error": str(e)}, status=500) 
    
    
    
    
@csrf_exempt
def generate_broadcaster_qrcode(request):
   
    url = "https://api.lovense-api.com/api/lan/getQrCode"
    d_token = settings.LOVENSE_DEV_KEY
    
    utoken = User_Data.objects.get(User = request.user)
    data = {
        "token":d_token,
        "uid": request.user.id,
        "uname": request.user.username,
        "utoken": utoken.U_token,
        "v": 2,
            }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Make the POST request using the requests library
        response = requests.post(url, json=data, headers=headers)

        # Check the response status code for success (e.g., 200)
        if response.status_code == 200:
            # Handle the successful response data
            response_data = response.json()
            
            return JsonResponse(response_data)

        # Handle other status codes if needed
        else:
            return JsonResponse({"error": "Failed to make the POST request."}, status=response.status_code)

    except requests.exceptions.RequestException as e:  
        return JsonResponse({"error": str(e)}, status=500) 
    


def invite_private_chat(request):
    
    if request.method == "POST":
        
        user_id = request.POST.get('user_id')
        broadcaster_id = request.POST.get('room_id')
        
        broadcaster = User.objects.get(id = broadcaster_id)
        user = User.objects.get(id = user_id)
        
        if Private_Chat_Invitee.objects.filter(broadcaster = broadcaster).exists():
            broadcaster = Private_Chat_Invitee.objects.get(broadcaster = broadcaster)
            broadcaster_invitee_list = broadcaster.Invitee.all()
            if user not in broadcaster_invitee_list:
                broadcaster.Invitee.add(user)
                invitee_instance = Private_Chat_Invitee.objects.get(Invitee=user)
                invitee_instance.Is_Sent_Invite = True
        else:
            broadcaster = Private_Chat_Invitee.objects.create(broadcaster=broadcaster)
            broadcaster.Invitee.add(user)
            invitee_instance = Private_Chat_Invitee.objects.get(Invitee=user)
            invitee_instance.Is_Sent_Invite = True

        
        
        
    
    return JsonResponse('OK', safe=False)


def trigger_toy(broadcaster_id,price,user_id,feature,strength,timesec):
    
    url = "https://api.lovense-api.com/api/lan/v2/command"
    d_token = settings.LOVENSE_DEV_KEY

    data = {
        "token":d_token,
        "uid": broadcaster_id,
        "command":"Pattern",
        "rule":"V:1,F:" + str(feature) + ";" + "S:1000#",
        "strength": str(strength),
        "timeSec": timesec * 60,
        "apiVer": 2,
            }     
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
   
            # Handle the successful response data
            response_data = response.json()
            
            player = User_Data.objects.get(User=user_id)
            player.Vibez = player.Vibez - price
            player.save()
            
            return JsonResponse({'data': response_data},safe=False)
        else:

            return JsonResponse({"error": "Failed to make the POST request."}, status=response.status_code)

    except requests.exceptions.RequestException as e:  
        return JsonResponse({"error": str(e)}, status=500) 
    
    return JsonResponse({"data": str(response.status_code)}, status=500) 

def fav_btn_trigger_toy(request):
    
    if request.method == "POST":
        room_data = Room_Data.objects.get(User=request.POST.get('room_id'))
        user_id = User.objects.get(id = request.POST.get('user_id'))
        
        button_type = request.POST.get('button_type')
        
        if str(button_type) == "mmm":
          
            broadcaster_id = room_data.User_id
            price = room_data.Price_MMM_button
            user_id = user_id.id
            feature = room_data.Feature_MMM_button
            strength = room_data.Strength_MMM_button
            timesec = room_data.Duration_MMM_button

            # Call the trigger_toy() function with the extracted attributes
            trigger_toy(broadcaster_id, price, user_id, feature, strength, timesec)
             
        if str(button_type) == "oh":
            
            broadcaster_id = room_data.User_id
            price = room_data.Price_OH_button
            user_id = user_id.id
            feature = room_data.Feature_OH_button
            strength = room_data.Strength_OH_button
            timesec = room_data.Duration_OH_button

            # Call the trigger_toy() function with the extracted attributes
            trigger_toy(broadcaster_id, price, user_id, feature, strength, timesec)
            
        if str(button_type) == "ohyes":
            
            broadcaster_id = room_data.User_id
            price = room_data.Price_OHYes_button
            user_id = user_id.id
            feature = room_data.Feature_OHYes_button
            strength = room_data.Strength_OHYes_button
            timesec = room_data.Duration_OHYes_button

            # Call the trigger_toy() function with the extracted attributes
            trigger_toy(broadcaster_id,price, user_id, feature, strength, timesec)
        
        return JsonResponse({'data': "success"},safe=False)
    


def get_invitees(request):
    
   if Private_Chat_Invitee.objects.filter(broadcaster=request.user).exists():
        broadcaster = Private_Chat_Invitee.objects.get(broadcaster=request.user)
        invitee_list = broadcaster.Invitee.all()
        
        invitees = []
        for invitee in invitee_list:
            
            if invitee.Is_Accepted_Invite == False:
                    invitees.append({
                        'user_id': invitee.id,
                        'name'  : invitee.username,
                    })
            
        
        return JsonResponse({"data":invitees}, safe=False)
    
    
def accept_privatechat(request):
    
    if request.method == "POST":
        user_id = User.objects.get(id = request.POST.get('user_id'))
        
        broadcaster = Private_Chat_Invitee.objects.get(broadcaster=request.user)
        for invitee in broadcaster.Invitee.all():
            if invitee == user_id:
                invitee.Is_Accepted_Invite = True
                invitee.save()
  
        
        return JsonResponse({'data':"success"}, safe=False)
    
    
@csrf_exempt
def Visitor(request):
    
    if request.method == "POST":
        
        user_id = int(request.POST.get('user_id'))
        room_id = int(request.POST.get('room_id'))
        leaving = request.POST.get('leaving')
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_visitors_{room_id}',
            {
                'user_id': user_id,
                'leaving': leaving,
            }
        )
        
        # try:
            
        #     Room_Visitors.objects.get(User=user_instance)
            
        # except Room_Visitors.DoesNotExist:
        #     room_visitor = Room_Visitors.objects.create(User=user_instance)
        #     # Add the visitor instance to the room's visitors
        #     room_instance.Visitors.add(room_visitor)
        #     room_instance.save()
            
        return JsonResponse({'data':"created"}, safe=False)
            
        
    

