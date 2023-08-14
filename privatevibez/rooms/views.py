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
from .forms import Slot_MachineForm, Fav_vibezForm, BioForm
from django.http import HttpResponse as httpresponse
import requests
from .decorators import check_user_blocked_ip
from accounts.forms import CustomPasswordChangeForm
from cryptography.fernet import Fernet
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .serializers import Private_Chat_InviteeSerializer, CountrySerializer, RegionSerializer
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

def change_password(request):
    changepassform = CustomPasswordChangeForm(request.user)
    if request.method == 'POST':
        changepassform = CustomPasswordChangeForm(request.user, request.POST)
        if changepassform.is_valid():
            user = changepassform.save()
            update_session_auth_hash(request, user)  # Important to update the session's auth hash
            return redirect('password_change_done')
    else:
        changepassform = CustomPasswordChangeForm(request.user)
        return changepassform



def user_blocked(request):
    return render(request, 'rooms/user_blocked.html')



#check if user's region or country is not blocked by the room
@check_user_blocked_ip(redirect_url="/room/blocked/404/")
def Room(request, Broadcaster):

    if request.user.is_authenticated:
             
            user_datas        = User_Data.objects.get(User =  request.user)
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
                    
                    availed_items = Item_Availed.objects.filter(Room = room_data).all()
                    print(availed_items,flush=True)
                    countries = Country.objects.all()
                    room_data_blocked_countries = room_data.Blocked_Countries.all()

                    # Extract a list of blocked country IDs
                    blocked_country_ids = room_data_blocked_countries.values_list('Country_id', flat=True)

                    # Filter countries based on blocked country IDs
                    filtered_countries = countries.exclude(id__in=blocked_country_ids)

                    regions = Region.objects.all()
                    room_data_blocked_regions = room_data.Blocked_Regions.all()
    
                    
                    blocked_region_ids = room_data_blocked_regions.values_list('Region_id', flat=True)
                    filtered_regions = regions.exclude(id__in=blocked_region_ids)

                    change_password(request)
                    # change_email(request)
                    
                    if Slot_Machine.objects.filter(User=request.user).exists():
                        slot_machine_data = Slot_Machine.objects.filter(User=request.user).values('Slot_cost_per_spin', 'Win_3_of_a_kind_prize', 'Win_2_of_a_kind_prize').get()
                
                
            except User_Status.DoesNotExist:
                messages.error(request, 'User does not exist')
    
    else:
        room_data = Room_Data.objects.get(User = User.objects.get(username = Broadcaster))

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
    print(request.POST.get('PrivateChatPrice'),flush=True)
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
            try:
                existing_instance = Slot_Machine.objects.get(
                    User=request.user
                )
                
                print("existing", flush=True)
                existing_instance.Slot_cost_per_spin = form.cleaned_data['Slot_cost_per_spin']
                existing_instance.Win_3_of_a_kind_prize = form.cleaned_data['Win_3_of_a_kind_prize']
                existing_instance.Win_2_of_a_kind_prize = form.cleaned_data['Win_2_of_a_kind_prize']
                existing_instance.save()
                messages.success(request, "Slot Machine saved successfully")
                # A duplicate instance already exists
                # Handle the case where a duplicate is found
            except Slot_Machine.DoesNotExist:
                # No duplicate instance found, proceed to save
                instance = form.save(commit=False)
                instance.User = request.user
                instance.save()
                messages.success(request, "Slot Machine saved successfully")
        else:
            messages.error(request, "Something went wrong")
            print(form.errors, flush=True)

        return redirect(request.META.get('HTTP_REFERER'))


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


def availed_item(user,room_id,item,price):
    user_data = User_Data.objects.get(User=user)
    room = Room_Data.objects.get(User_id=room_id)
    item = Item_Availed.objects.create(Room=room,User=user,Item=item, Cost=price)
    user_data.Availed.add(item)
    
    # add revenues
    if room.Revenue is not None:
        room.Revenue = room.Revenue + int(price)
    else:
        room.Revenue = int(price)
    room.save()
    
    # Get the channel layer
    channel_layer = get_channel_layer()
    channel_name = "broadcaster_visitor_" + str(room_id)
    print(channel_name,flush=True)
    
    # Prepare data to send
    data = {
        "user": user.username,
        "item": item.Item,
        "price": item.Cost  # Changed "Cost" to "Price"
    }
    
    # Send the data to the WebSocket consumer
    async_to_sync(channel_layer.group_send)(
        channel_name,
        {"type": "show.itemAvailed", "data": data}
    )
    

def fav_btn_trigger_toy(request):
    
    if request.method == "POST":
        room_data = Room_Data.objects.get(User=request.POST.get('room_id'))
        user_id = User.objects.get(id = request.POST.get('user_id'))
        
        button_type = request.POST.get('button_type')
        
        if str(button_type) == "mmm":
            
            availed_item(user_id,room_data.User_id,"MMM",room_data.Price_MMM_button)
            
            
            broadcaster_id = room_data.User_id
            price = room_data.Price_MMM_button
            user_id = user_id.id
            feature = room_data.Feature_MMM_button
            strength = room_data.Strength_MMM_button
            timesec = room_data.Duration_MMM_button

            # Call the trigger_toy() function with the extracted attributes
            trigger_toy(broadcaster_id, price, user_id, feature, strength, timesec)
             
        if str(button_type) == "oh":
            
            availed_item(user_id,room_data.User_id,"OH",room_data.Price_OH_button)
            
            broadcaster_id = room_data.User_id
            price = room_data.Price_OH_button
            user_id = user_id.id
            feature = room_data.Feature_OH_button
            strength = room_data.Strength_OH_button
            timesec = room_data.Duration_OH_button

            # Call the trigger_toy() function with the extracted attributes
            trigger_toy(broadcaster_id, price, user_id, feature, strength, timesec)
            
        if str(button_type) == "ohyes":
            
            
            availed_item(user_id,room_data.User_id,"OHYes",room_data.Price_OHYes_button)
            
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
            
        
    
@csrf_exempt
def search_countries(request):
        
        if request.method == "GET":
            country = request.GET.get('search')
            if country is not None:
                country = Country.objects.filter(name__icontains=country)
                serializer = CountrySerializer(country, many=True)
                return JsonResponse({'data':serializer.data}, safe=False)
            else:
                return JsonResponse({'data':"empty"}, safe=False)
        else:
            return JsonResponse({'data':"none"}, safe=False)

    
@csrf_exempt
def search_regions(request):
        
        if request.method == "GET":
            region = request.GET.get('search')
            region = Region.objects.filter(display_name__icontains=region)
            serializer = RegionSerializer(region, many=True)
            
            return JsonResponse({'data':serializer.data}, safe=False)
        else:
            return JsonResponse({'data':"none"}, safe=False)


def update_room_rules(request):
    
    
    if request.method == 'POST':
        
        room_id = request.user
        room_instance = Room_Data.objects.get(User=room_id)
        rules = request.POST.get('room_rules')
        if rules is not None:
            room_instance.Room_Rules = request.POST.get('room_rules')
            room_instance.save()
     
            return JsonResponse({"data":"Room rules updated"},safe=False)
        else:
        
            return JsonResponse({"data":"Room rules is empty"}, safe=False)
    
    
    
def submit_bio(request):
    
    if request.method == 'POST':
        form = BioForm(request.POST,request.FILES)
        
        if form.is_valid():
            user = request.user
            goal_vibez = form.cleaned_data['goal_vibez']
            username = form.cleaned_data['username']
            real_name = form.cleaned_data['real_name']
            I_am = form.cleaned_data['I_am']
            Interested_In = form.cleaned_data['Interested_In']
            Location = form.cleaned_data['Location']
            Language = form.cleaned_data['Language']
            Body_Type = form.cleaned_data['Body_Type']
            profile_pic = form.cleaned_data['profile_pic']
            
            room_data = Room_Data.objects.get(User=user)
            
            room_data.Goal = goal_vibez
            room_data.save()
            
            user_data = User_Data.objects.get(User=user)
            user.username = username
            user.save()
            
            user_data.Real_Name = real_name
            user_data.I_am = I_am
            user_data.Interested_In = Interested_In
            user_data.Location = Location
            user_data.Language = Language
            user_data.Body_Type = Body_Type
            
            if profile_pic is not None:
                user_data.Profile_Pic = profile_pic
                user_data.save()
        else:
            print(form.errors,flush=True)
        print(form,flush=True)
        return JsonResponse({'data':"success"}, safe=False)
    
    
    

def save_hashtags(request):
    
    if request.method == "POST":
        hashtags = request.POST.get('hashtags')
        if hashtags is not None:
            room_data = Room_Data.objects.get(User=request.user)
            room_data.hashtags = hashtags
            room_data.save()
            return JsonResponse({'data':"Hashtags successfully saved!"}, safe=False)
        else:
            return JsonResponse({'data':"Hashtags is empty."}, safe=False)
        
     