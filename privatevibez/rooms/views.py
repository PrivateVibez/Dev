from django.shortcuts import render
from django.contrib.auth.models import User
from rooms.models import *
from accounts.models import *
from chat.models import *
from django.utils import timezone
from datetime import date
from django.contrib.sessions.models import Session
from cities.models import City, Country, Region
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from staff.models import PrivatevibezRevenue
from django.utils.safestring import mark_safe
import json
import random
from datetime import datetime
from .forms import Slot_MachineForm, Fav_vibezForm, BioForm, MenuDataForm
from django.http import HttpResponse as httpresponse
import requests
from .decorators import check_user_blocked_ip,check_user_status
from accounts.forms import CustomPasswordChangeForm
from cryptography.fernet import Fernet
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .serializers import Private_Chat_InviteeSerializer, CountrySerializer, RegionSerializer, SlotMachineSerializer, Item_AvailedSerializer
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import transaction, IntegrityError
from django.db.models import Q, F
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
@check_user_blocked_ip(redirect_url="/room/notfound/404/")
# @check_user_status(redirect_url="/")
def Room(request, Broadcaster):

    if request.user.is_authenticated:
            try:
                user_datas        = User_Data.objects.get(User =  request.user)
            except User_Data.DoesNotExist:
                pass
            

            if request.user.username == Broadcaster:
                check_user_status = User.objects.get(username = Broadcaster)
                is_broadcaster_room = True
                if check_user_status.Status == "Broadcaster":
                    is_broadcaster = True
                if check_user_status.Status == "Pending_Broadcaster":
                    is_pending_broadcaster = True
                if check_user_status.Status == "Declined_Broadcaster":
                    is_declined_broadcaster = True
                    
                
            else:
                check_user_status = User.objects.get(username = request.user.username)
                
                is_broadcaster_room = False
                if check_user_status.Status == "Broadcaster":
                    is_broadcaster = True
                if check_user_status.Status == "Pending_Broadcaster":
                    is_pending_broadcaster = True
                if check_user_status.Status == "Declined_Broadcaster":
                    is_declined_broadcaster = True
                    
            try:
                
                with transaction.atomic():
                    if User.objects.filter(username =  Broadcaster, Status = "Broadcaster").exists():
                            user_status_data = User.objects.get(id = request.user.id)
                            user_status      = user_status_data.Status
                            broadcaster_user     = User.objects.get(username = Broadcaster)
                            room_name_json       = mark_safe(json.dumps(broadcaster_user.username))
                            room_name            = broadcaster_user.username
                            username             = mark_safe(json.dumps(request.user.username))
                            rooms                = Room_Data.objects.all()
                            room_users_data      = User_Data.objects.all()    
                            menu_data            = Menu_Data.objects.filter(User = broadcaster_user)
                            broadcaster_status   = User_Status.objects.get(User = User.objects.get(username = Broadcaster))
                            room_data            = Room_Data.objects.get(User = User.objects.get(username = Broadcaster))
                            # room_sesson          = Room_Sesson.objects.get(User = User.objects.get(username = Broadcaster))
                            broadcaster_data     = User_Data.objects.get(User = User.objects.get(username = Broadcaster))
                            availed_items = Item_Availed.objects.filter(Room=room_data, Timestamp__date=timezone.now().date()).all()
                            subscriptions        = Subscription.objects.all()
                        
                            private_chat = Private.objects.filter(
                                Q(From=request.user, To=broadcaster_user) | Q(To=request.user, From=broadcaster_user)
                            ).order_by('Timestamp')

                                
                            public_chat          = Public.objects.filter(Room = User.objects.get(username=Broadcaster)).all
                            follows              = Follows.objects.filter(User__username = request.user.username).all()
                            
                            thumbs_up_count      = Thumbs.objects.filter(Broadcaster = User.objects.get(username = Broadcaster), Thumb = "Up").count
                            thumbs_down_count    = Thumbs.objects.filter(Broadcaster = User.objects.get(username = Broadcaster), Thumb = "Down").count
                            if Thumbs.objects.filter(User = request.user,Broadcaster = User.objects.get(username = Broadcaster),Thumb = "Up").exists():
                                thumbs_up_color  = True
                            else:
                                thumbs_up_color  = False
                            if Thumbs.objects.filter(User = request.user,Broadcaster = User.objects.get(username = Broadcaster),Thumb = "Down").exists():
                                thumbs_Down_color  = True
                            else:
                                thumbs_Down_color  = False

                            if Follows.objects.filter(User = request.user, Broadcaster=broadcaster_user.id).exists():
                                follow_button = True
                            else:
                                follow_button = False
                                
                                
                            if Slot_Machine.objects.filter(User=broadcaster_user).exists():
                                    slot_machine_cost_per_spin = Games_Data.objects.order_by('-timestamp').values('Slot_Machine_Spin_Cost').first()
                                    lottery_cost_per_spin = Games_Data.objects.order_by('-timestamp').values('Lottery_Spin_Cost').first()
                                    dice_cost_per_spin = Games_Data.objects.order_by('-timestamp').values('Dice_Spin_Cost').first()
                                    
                                    
                                    slot_machine_data = Slot_Machine.objects.filter(User=broadcaster_user.id).values('pot', 'Win_3_of_a_kind_prize', 'Win_2_of_a_kind_prize').get()
                            try:
                                user = request.user

                                if user.Status == "User":

                                    try:
                            
                                        private_chat_invite = Private_Chat_Invitee.objects.get(Broadcaster=broadcaster_user, Invitee_relationships__Invitee=user)   
                                        invitees = private_chat_invite.Invitee_relationships.all()
                                        
                                        for invitee in invitees:
                                            if invitee.Invitee == user:
                                                    invite_accepted = True if invitee.Is_Accepted == True else False
                                    except Private_Chat_Invitee.DoesNotExist:
                                        pass
                                    
                                    
                                    try:
                                        user_spendings = Item_Availed.objects.filter(User=request.user)
                                        total_user_spendings = sum(int(item.Cost) for item in user_spendings)

                                        
                                    except Item_Availed.DoesNotExist:
                                        
                                        pass

                                    
                                                
                    
                                elif user.Status == "Broadcaster":
                                    
                                    # LOTTERY PRIZES
                                    lottery_prizes_list = ['MMM','OH','OHYes']

                                    # Loop through the queryset and append the values to the list
                                    for item in menu_data:
                                        lottery_prizes_list.append(item.Menu_Name)
                                                                        
                                    lottery_slot_1 = Lottery.objects.get(User=broadcaster_user, slot_number=1) if Lottery.objects.filter(User=broadcaster_user, slot_number=1).exists() else None
                                    lottery_slot_2 = Lottery.objects.get(User=broadcaster_user, slot_number=2) if Lottery.objects.filter(User=broadcaster_user, slot_number=2).exists() else None
                                    lottery_slot_3 = Lottery.objects.get(User=broadcaster_user, slot_number=3) if Lottery.objects.filter(User=broadcaster_user, slot_number=3).exists() else None
                                    lottery_slot_4 = Lottery.objects.get(User=broadcaster_user, slot_number=4) if Lottery.objects.filter(User=broadcaster_user, slot_number=4).exists() else None
                                    lottery_slot_5 = Lottery.objects.get(User=broadcaster_user, slot_number=5) if Lottery.objects.filter(User=broadcaster_user, slot_number=5).exists() else None
                                    lottery_slot_6 = Lottery.objects.get(User=broadcaster_user, slot_number=6) if Lottery.objects.filter(User=broadcaster_user, slot_number=6).exists() else None
                                    lottery_slot_7 = Lottery.objects.get(User=broadcaster_user, slot_number=7) if Lottery.objects.filter(User=broadcaster_user, slot_number=7).exists() else None
                                    lottery_slot_8 = Lottery.objects.get(User=broadcaster_user, slot_number=8) if Lottery.objects.filter(User=broadcaster_user, slot_number=8).exists() else None
                                                                        
                                    dice_1 = Dice.objects.get(User=broadcaster_user, dice_number=1) if Dice.objects.filter(User=broadcaster_user, dice_number=1).exists() else None
                                    dice_2 = Dice.objects.get(User=broadcaster_user, dice_number=2) if Dice.objects.filter(User=broadcaster_user, dice_number=2).exists() else None
                                    dice_3 = Dice.objects.get(User=broadcaster_user, dice_number=3) if Dice.objects.filter(User=broadcaster_user, dice_number=3).exists() else None
                                    dice_4 = Dice.objects.get(User=broadcaster_user, dice_number=4) if Dice.objects.filter(User=broadcaster_user, dice_number=4).exists() else None
                                    dice_5 = Dice.objects.get(User=broadcaster_user, dice_number=5) if Dice.objects.filter(User=broadcaster_user, dice_number=5).exists() else None
                                    dice_6 = Dice.objects.get(User=broadcaster_user, dice_number=6) if Dice.objects.filter(User=broadcaster_user, dice_number=6).exists() else None
           
                    
                                    if Private_Chat_Invitee.objects.filter(Broadcaster=request.user).exists():
                                        private_chat_invite = Private_Chat_Invitee.objects.get(Broadcaster=request.user)
                                        pending_private_chat_invitees = private_chat_invite.Invitee_relationships.filter(Is_Accepted=False).count()
                                        all_pending_private_chat_invitees = private_chat_invite.Invitee_relationships.filter(Is_Accepted=False)
                                        
                                        invitees = private_chat_invite.Invitee_relationships.all()
                                        
                                        fan_list = []
                                        fan_list_names = []
                                        
                                        for fan in invitees:
                                            if fan.Is_Accepted == True:
                                                print(fan,flush=True)
                                                fan_list.append({
                                                    'user_id': fan.Invitee.id,
                                                    'name': fan.Invitee.username,
                                                })
                                                fan_list_names.append(fan.Invitee.username)
                                                
                                        fan_list_json = json.dumps(fan_list)
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
                                    
                                            
                                    
                                    broadcaster_followers_details = get_broadcaster_followers(broadcaster_user)                                    
                                    
                                    if Slot_Machine.objects.filter(User=user).exists():
                        
                                        slot_machine_data = Slot_Machine.objects.filter(User=user).values('pot', 'Win_3_of_a_kind_prize', 'Win_2_of_a_kind_prize').get()
                                        
                                        

                                
                                return render(request, "rooms/home.html", locals()) 
                            except User_Status.DoesNotExist:
                                messages.error(request, 'User does not exist')
                    
                    else:
                        if User.objects.filter(username =  Broadcaster).exists():
                            user = User.objects.get(username = Broadcaster)
                            user_status = user.Status
                            room_data = Room_Data.objects.get(User = User.objects.get(username = Broadcaster))
                            print(user_status,flush=True)
                            return render(request, "rooms/home.html", locals())
                        else:
                            print("user does not exist",flush=True)
                            return render(request,'rooms/userdoesnotexist.html')
                        
            except IntegrityError as e:
                print(e,flush=True)
    else:
        room_data = Room_Data.objects.get(User = User.objects.get(username = Broadcaster))
        return render(request, "rooms/home.html", locals())



def get_broadcaster_followers(broadcaster):
    
    broadcaster_followers = Follows.objects.filter(Broadcaster=broadcaster)

    # Extract the follower users from the queryset
    follower_users = broadcaster_followers.values_list('User', flat=True).distinct()

    # Filter Item_Availed objects based on the followers
    broadcaster_followers_details = []
    
    print(follower_users,flush=True)
    
    for user in follower_users:
        
        item_availed = Item_Availed.objects.filter(User=user).first()  # Assuming you want one item per user

        broadcaster_followers_details.append({
            
                'username': item_availed.User.username,
                'status': is_user_online(broadcaster,item_availed.User),
                'sent_vibez': get_total_user_spendings(item_availed.User,["Sent Vibez"]),
                'total_menuitems_spending': get_total_user_spendings(item_availed.User),
                'total_slots_spending': get_total_user_spendings(item_availed.User,["Slot Spin","2OAK","3OAK"]),
                'total_buttons_availed': get_total_user_spendings(item_availed.User,["MMM","OHYes","OH"]),
            
         }),
    
    print(broadcaster_followers_details,flush=True)
    
    return broadcaster_followers_details
    
    

def get_total_user_spendings(user,item=""):
        
        if item != "":
            user_spendings = Item_Availed.objects.filter(User=user,Item__in=item)
            total_user_spendings = sum(int(item.Cost) for item in user_spendings)
        else:
            user_spendings = Item_Availed.objects.filter(User=user).exclude(Item__in=["Sent Vibez","Slot Spin","2OAK","3OAK","MMM","OHYes","OH"])
            total_user_spendings = sum(int(item.Cost) for item in user_spendings)
            
        return total_user_spendings

def is_user_online(broadcaster,user):
    try:
        
        expiration_datetime = timezone.now() - timezone.timedelta(seconds=settings.SESSION_COOKIE_AGE)


        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())      
        
        user_sessions = []  
        
        for s in active_sessions:
            
            if Follows.objects.filter(Broadcaster=broadcaster,
                    User__pk=s.get_decoded().get('_auth_user_id')
                ).exists():
                user_sessions.append(s)
                
                print(s,flush=True)
        
         
        for session in user_sessions:
            user_id = session.get_decoded().get('_auth_user_id')
       
            if int(user_id) == user.id:
                return True
            else:
                return False

            

 # User is considered online if they have been active in the last 15 minutes
    except Session.DoesNotExist:
 
        return False


@csrf_exempt
def save_menu_data(request):
    
    if request.method == "POST":
        form = MenuDataForm(request.POST)
        
        if form.is_valid():
            
            Menu_Data.objects.create(
                User       = request.user,
                Vibez_Cost  =  form.cleaned_data['menu_item_price'],
                Menu_Name   = form.cleaned_data['menu_item'],
                Menu_Time   =  form.cleaned_data['menu_item_duration']
            )
            return JsonResponse({"data":f'menu item added!'}, safe=False) 
        else:
            print(form.errors,flush=True)
            return JsonResponse({"data":"please input valid data"},status=500, safe=False) 
    
    

@csrf_exempt
def avail_menu_item(request):
    
    if request.method == "POST":
        
        menu_item_id = request.POST.get('menu_item_id')
        broadcaster_id = request.POST.get('broadcaster_id')
        
        if menu_item_id is not None and broadcaster_id is not None:
            
            try:
                
                menu_item = Menu_Data.objects.get(id=menu_item_id)
                broadcaster_room = Room_Data.objects.get(User__id = broadcaster_id)
                item = Item_Availed.objects.create(Room = broadcaster_room,User=request.user, Item = menu_item.Menu_Name, Cost = menu_item.Vibez_Cost)
                
                user = User_Data.objects.get(User = request.user)
                
                if user.Vibez >= menu_item.Vibez_Cost:
                    user.Vibez = user.Vibez - menu_item.Vibez_Cost
                    
                    if broadcaster_room.Revenue != None:
                        broadcaster_room.Revenue += menu_item.Vibez_Cost
                    else:
                        broadcaster_room.Revenue = menu_item.Vibez_Cost
                    
                    
                    user.save()
                    broadcaster_room.save()
                    
                    display_user_availed_item_in_broadcaster_room(user,item,broadcaster_room)
                    
                    
                    return JsonResponse({"data":f'you bought {menu_item.Menu_Name} lets keep vibing!'}, safe=False)
                else:
                    return JsonResponse({"data":f'not enough vibez'}, status=500, safe=False)
            except IntegrityError as e:
                
                print(e,flush=True)
                
        else:
            return JsonResponse({"data":f'please input a valid data'},status=500, safe=False)
                
                

@csrf_exempt
def update_menu_data(request):
    
    if request.method == "POST":
        form = MenuDataForm(request.POST)
        
        if form.is_valid():
            
            menu_data = Menu_Data.objects.get(id = request.POST.get('item_id'))
            
            menu_data.Vibez_Cost  =  form.cleaned_data['menu_item_price']
            menu_data.Menu_Name   = form.cleaned_data['menu_item']
            menu_data.Menu_Time   =  form.cleaned_data['menu_item_duration']
            
            menu_data.save()
            return JsonResponse({"data":f'menu item updated!'}, safe=False) 
        else:
            print(form.errors,flush=True)
            return JsonResponse({"data":form.errors}, status=500, safe=False) 
        
    else:
        
        return JsonResponse({"data":f'something went wrong.'}, status=500, safe=False) 
        
@csrf_exempt
def remove_menu_data(request):
    
    if request.method == "POST":

        Menu_Data.objects.get(id = request.POST.get('item_id')).delete()
        
        return JsonResponse({"data":"menu item deleted!"}, safe=False) 

    else:
        
        return JsonResponse({"data":f'something went wrong.'}, status=500, safe=False) 
    

@csrf_exempt
def Dice_items(request):
    
    try:
           
        with transaction.atomic():
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
    except IntegrityError as e:
        
        print(e,flush=True)


@csrf_exempt
def Following(request):
    broadcaster = request.POST.get('broadcaster')
    
    try:
        
        with transaction.atomic():
            if Follows.objects.filter(User = request.user,Broadcaster__username=broadcaster).exists():
                if Follows.objects.filter(Broadcaster = User.objects.get(username = broadcaster)).exists():

                    Del_flow = Follows.objects.get(User = request.user, Broadcaster = User.objects.get(username = broadcaster) )
                    Del_flow.delete()
                    message = f'You have unfollowed {broadcaster}'
                else:
                    Follows.objects.create(
                        User         =  request.user,
                        Broadcaster   =   User.objects.get(username = broadcaster)
                    )
                    message = f'You are now following {broadcaster}'
            else:
                    Follows.objects.create(
                        User         =  request.user,
                        Broadcaster   =   User.objects.get(username = broadcaster)
                    )
                    message = f'You are now following {broadcaster}'
                    
            return JsonResponse({'data':message}, safe=False) 
        
    except IntegrityError as e:
        
        print(e,flush=True)


def Thumb(request):
    
    try:
        
        with transaction.atomic():
            
            if Thumbs.objects.filter(User = request.user).exists():
                if Thumbs.objects.filter(Broadcaster = User.objects.get(username = request.POST.get('broadcaster'))).exists():
                    
                        thumb = Thumbs.objects.get(User = request.user, Broadcaster = User.objects.get(username = request.POST.get('broadcaster')) )
                        
                        print(thumb.Thumb,flush=True)
                        print(request.POST.get('Thumb'),flush=True)
                        
                        if thumb.Thumb == "Down" and request.POST.get('Thumb') == "Down" or thumb.Thumb == "Up" and request.POST.get('Thumb') == "Up":
                            thumb.delete()
                            
                        else:
                            if request.POST.get('Thumb') == "Down":
                                thumb.Thumb = "Down"
                                thumb.save()
                            else:
                                thumb.Thumb = "Up"
                                thumb.save()

                            
            
                else:
                    if request.POST.get('Thumb') == "Down":
                        Thumbs.objects.create(
                            User         =  request.user,
                            Broadcaster   =   User.objects.get(username = request.POST.get('broadcaster')),
                            Thumb        =   "Down"
                        )
                    else:
                        Thumbs.objects.create(
                            User         =  request.user,
                            Broadcaster   =   User.objects.get(username = request.POST.get('broadcaster')),
                            Thumb        =   "Up"
                        )
            else:
                if request.POST.get('Thumb') == "Down":
                    Thumbs.objects.create(
                        User         =  request.user,
                        Broadcaster   =   User.objects.get(username = request.POST.get('broadcaster')),
                        Thumb        =   "Down"
                    )
                else:
                    Thumbs.objects.create(
                        User         =  request.user,
                        Broadcaster   =   User.objects.get(username = request.POST.get('broadcaster')),
                        Thumb        =   "Up"
                    )
            return JsonResponse('OK', safe=False) 
        
    except IntegrityError as e:
            
            print(e,flush=True)
            
            
def PrivateChatCheckBox(request):
    
    if request.POST.get('Checked') is not None:
        
        room_data = Room_Data.objects.get(User = request.user)
        room_data.Private_Chat = request.POST.get('Checked')
        room_data.save()
        return JsonResponse('OK', safe=False) 
    else:
        return JsonResponse({'data':f'something went wrong'},status=500, safe=False) 

def PublicChatCheckBox(request):
    
    if request.POST.get('Checked') is not None:
        
        room_data = Room_Data.objects.get(User = request.user)
        room_data.Public_Chat = request.POST.get('Checked')
        room_data.save()
        return JsonResponse('OK', safe=False) 
    
    else:
        return JsonResponse({'data':f'something went wrong'},status=500, safe=False) 

def Chat(request):

    try:
        
        room_data = Room_Data.objects.get(User = request.user)
        room_data.Public_Chat = request.POST.get('Public_Chat_Check')
        room_data.Private_Chat_Price = int(request.POST.get('PrivateChatPrice'))
        room_data.save()
        return JsonResponse('OK', safe=False) 

    except Room_Data.DoesNotExist:
        return JsonResponse({'data':f'broadcaster does not exist'},status=500, safe=False)

def Save_RoomPatterns(request):
    
    try:
        with transaction.atomic():
            
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
    
    except IntegrityError as e:
        
        print(e,flush=True)


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
                
              
                existing_instance.pot = form.cleaned_data['pot']

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
        
        return JsonResponse({"data":f''}, safe=False)
    
    else:
        
        return JsonResponse({"data":f'something went wrong'},status=500, safe=False)

 
@csrf_exempt
def charge_user(cost):
    private_vibez = PrivatevibezRevenue.objects.order_by('timestamp').first()

    if private_vibez:
        # charge user per spin
        remaining_price = cost - private_vibez.Chargeback
        private_vibez.Slot_Machine_Revenue = private_vibez.Slot_Machine_Revenue + private_vibez.Chargeback
        private_vibez.save()   
        
        return remaining_price



def player_remaining_spins_or_vibez(winner,msg,pot,serializer=None):

    if winner.Free_spins != 0:
        spins = {"spins": winner.Free_spins}
        vibez = None
    else:
        vibez = {"vibez": winner.Vibez}
        spins = None

    data = {
        "msg": msg,
        "vibez": vibez if vibez is not None else None,
        "spins": spins if spins is not None else None,
        "pot": pot if pot is not None else None
    }
    
    return data


def random_favorite_button(room_data):
    
    buttons = ["OHYes", "OH", "MMM"]
    random_button = random.choice(buttons)
    
    if random_button == "OHYes":
        feature = room_data.Feature_OHYes_button
        strength = room_data.Strength_OHYes_button
        timesec = room_data.Duration_OHYes_button
        button_cost = room_data.Price_OHYes_button
        
    elif random_button == "OH":
        feature = room_data.Feature_OH_button
        strength = room_data.Strength_OH_button
        timesec = room_data.Duration_OH_button
        button_cost = room_data.Price_OH_button
    elif random_button == "MMM":
        feature = room_data.Feature_MMM_button
        strength = room_data.Strength_MMM_button
        timesec = room_data.Duration_MMM_button
        button_cost = room_data.Price_MMM_button
        
    return feature, strength, timesec, random_button, button_cost
    
    
@csrf_exempt
def get_prize(request):
    
    if request.method == 'POST':
        
            try:
                
                try:
                    with transaction.atomic():
                        winner = User_Data.objects.get(User__id=request.POST.get('winner'))
                        broadcaster = request.POST.get('broadcaster')
                        prize = request.POST.get('prize_won')
                        pot = int(request.POST.get('pot'))
                        cost_per_spin = int(request.POST.get('cost_per_spin'))
                        room_data = get_object_or_404(Room_Data, User_id=broadcaster)     
                        broadcaster_slot = Slot_Machine.objects.filter(User=room_data.User).first()

                
                except IntegrityError as e:
                    print(e,flush=True)
                    
                    
            except User_Data.DoesNotExist as e:
                return JsonResponse({'data':f'Broadcaster does not exist'},status=500, safe=False)
           
            if pot == broadcaster_slot.pot:
                if winner.Vibez >= cost_per_spin or winner.Free_spins != 0:
                    if prize == "2OAK":
                        
                        feature, strength, timesec, random_button, button_cost = random_favorite_button(room_data)
                        price = cost_per_spin
                        
                        note = f'{winner.User.username} Won Two of a kind! enjoy button {random_button}'
                        
                        deduct_spin_or_vibez(winner,room_data,price,game_type=None,game_data=None)


                        
                        pot = availed_item(winner.User.id,room_data,"2OAK",price,"Slot_Machine",random_button,button_cost,note)
                        
                        trigger_toy(room_data.User.id,price,winner.User.id,feature,strength,timesec)
                        
                        msg = f'Two of a kind!! {random_button}'
                        data = player_remaining_spins_or_vibez(winner,msg,pot)
                        
                        
                    if prize == "3OAK":
                        feature = room_data.Feature_OHYes_button
                        strength = room_data.Strength_OHYes_button
                        timesec = room_data.Duration_OHYes_button
                        price = cost_per_spin
                        note = f'{winner.User.username} Won Three of a kind!'
                
                        deduct_spin_or_vibez(winner,room_data,price,game_type=None,game_data=None)

                        pot = availed_item(winner.User.id,room_data,"3OAK",price,"Slot_Machine","30AK",room_data.Price_OHYes_button,note)
            
                        is_Jackpot = True
                        trigger_toy(room_data.User.id,price,winner.User.id,feature,strength,timesec,room_data,is_Jackpot)
                        
                        msg = f'JACPOT!!!!! crediting pot to {room_data.User.username}'
                        data = player_remaining_spins_or_vibez(winner,msg,pot)
                        
                    if prize == "Loss":
                        feature = room_data.Feature_OH_button
                        strength = room_data.Strength_OH_button
                        timesec = 1    
                            
                        deduct_spin_or_vibez(winner,room_data,cost_per_spin,game_type=None,game_data=None)
                        remaining_price = cost_per_spin
                        
                        availed_item(winner.User.id,room_data,"Slot Spin",remaining_price,"Slot_Machine","Loss")
                        trigger_toy(room_data.User.id,cost_per_spin,winner.User.id,feature,strength,timesec)
                        slot_machine_pot = Slot_Machine.objects.filter(User=room_data.User)
                        
                        for machine in slot_machine_pot:
                            machine.pot += remaining_price
                            machine.save()
                            pot = machine.pot
                    
                        serializer = SlotMachineSerializer(slot_machine_pot,many=True)
                        msg = f'You lose some, you win some. Keep vibing!'
                    
                        data = player_remaining_spins_or_vibez(winner,msg,pot)

                        return JsonResponse(data, status=500, safe=False)
                

                    
                    return JsonResponse({"data":data}, status=200, safe=False)
                
                
                else:
                    return JsonResponse({"error": f'Oops! not enough vibez!'}, status=500,safe=False) 
                    
                    # Handle other status codes if needed
            else:
                return JsonResponse({"error": f'Oops! cheater alert!'}, status=500,safe=False) 


    else:
        return JsonResponse({"error": "Failed to make the POST request."}, status=response.status_code)

    
    
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
        
        
        try:
            
            with transaction.atomic():
                
                broadcaster = User.objects.get(id = broadcaster_id)
                room_data = Room_Data.objects.get(User=broadcaster)
                broadcaster_private_chat = Room_Data.objects.get(User__id=broadcaster_id)
                broadcaster_private_chat_price = broadcaster_private_chat.Private_Chat_Price
                
                user = User_Data.objects.get(User=user_id)
                
                if Private_Chat_Invitee.objects.filter(Broadcaster = broadcaster).exists():
                    broadcaster = Private_Chat_Invitee.objects.get(Broadcaster = broadcaster)
                    invitee_relationship, _ = InviteeRelationship.objects.get_or_create(User=broadcaster.Broadcaster, Invitee=user.User)
                    broadcaster_invitee_list = broadcaster.Invitee_relationships.all()
                    


                    if user not in broadcaster_invitee_list:
                        
                        
                        if user.Vibez > broadcaster_private_chat_price:
                            user.Vibez -= broadcaster_private_chat_price
                            user.save()
                            
                            if room_data.Revenue != None:
                                room_data.Revenue += broadcaster_private_chat_price
                            else:
                                room_data.Revenue = broadcaster_private_chat_price
                            room_data.save()
                            broadcaster.Invitee_relationships.add(invitee_relationship)
                            
                            channel_layer = get_channel_layer()
                            channel_name = "fetch_private_chat_invitation_" + str(broadcaster.Broadcaster.username)
                            print(channel_name,flush=True)
                                
                                # Prepare data to send
                            data = {
                                "invitation_sent": True,
                            }
                            
                            # Send the data to the WebSocket consumer
                            async_to_sync(channel_layer.group_send)(
                                channel_name,
                                {"type": "is.InvitationSent", "data": data}
                            )
                            return JsonResponse({'data':"Invite sent!"},safe=False)
                        else:
                            return JsonResponse(f'not enough vibez!',status=500,safe=False)
                        
                        
                    

                

                            
                else:
                    broadcaster = Private_Chat_Invitee.objects.create(Broadcaster=broadcaster)
                    invitee_relationship, _ = InviteeRelationship.objects.get_or_create(User=broadcaster.Broadcaster, Invitee=request.user)
                    broadcaster.Invitee_relationships.add(invitee_relationship)
                    return JsonResponse({'data':"Invite sent!"},safe=False)
                
        except IntegrityError as e:
            
            print(e,flush=True)

                
                
                
            
        


def trigger_toy(broadcaster_id,price,user_id,feature,strength,timesec,room_data=None,is_Jackpot=False):
    
    if is_Jackpot == False:
        
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

                return JsonResponse({'data': response_data},safe=False)
            else:

                return JsonResponse({"error": "Failed to make the POST request."}, status=response.status_code)

        except requests.exceptions.RequestException as e:  
            return JsonResponse({"error": str(e)}, status=500) 
    
    else:
        
        
        url = "https://api.lovense-api.com/api/lan/v2/command"
        d_token = settings.LOVENSE_DEV_KEY

        data = {
            "token":d_token,
            "uid": broadcaster_id,
            "command":"Pattern",
            "rule":"V:1,F:" + str(room_data.Feature_MMM_button)  + ";"  + str(room_data.Feature_OH_button) + ";"  + str(room_data.Feature_OHYes_button) + ";" + "S:1000#",
            "strength": str(room_data.Strength_MMM_button)  + ";"  + str(room_data.Strength_OH_button) + ";"  + str(room_data.Strength_OHYes_button),
            "timeSec": 120,
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
                
                return JsonResponse({'data': response_data},safe=False)
            else:

                return JsonResponse({"error": "Failed to make the POST request."}, status=response.status_code)

        except requests.exceptions.RequestException as e:  
            return JsonResponse({"error": str(e)}, status=500) 
        
  

# GIVE PROFIT TO BROADCASTER AND SHOW IT TO THE BROADCASTER ROOM
def display_user_availed_item_in_broadcaster_room(user_data,item,room,random_button=None,button_cost=None,remaining_price=None):
    # Get the channel layer
    slot_machine = Slot_Machine.objects.filter(User=room.User).first()
    pot = slot_machine.pot

    
    if item.Item == "3OAK":
        print(item,flush=True)
        if slot_machine:
            # Retrieve values from the Slot_Machine object
            
                
            # Calculate the new revenue value
            new_revenue = room.Revenue + pot 
                
            # Update the room's revenue
            if room.Revenue is not None:
                room.Revenue += new_revenue - 100
               
            else:
                room.Revenue = new_revenue - 100
    
                
            room.save()
            
                
                
             # Make sure to save the room object

            # Update the Slot_Machine object's pot_increase
            slot_machine.pot = 100
            slot_machine.save()
            
            slot_machine_instance = slot_machine.pot
            show_item_in_roomstats(room,user_data,item)
            return slot_machine_instance
            
    elif item.Item == "2OAK":

        print(random_button,flush=True)
        print(button_cost,flush=True)
        if random_button != None and button_cost != None:
            remaining_pot = pot - button_cost
            
            # Update the room's revenue
            if room.Revenue is not None:
                room.Revenue += button_cost
               
            else:
                room.Revenue = button_cost
    
                
            room.save()
            
            slot_machine.pot = remaining_pot
            slot_machine.save()
            
            slot_machine_instance = slot_machine.pot
            show_item_in_roomstats(room,user_data,item)
            return slot_machine_instance
            
        else:
        
            slot_machine_instance = None
            
    else:
        slot_machine_instance = None
        
        show_item_in_roomstats(room,user_data,item)
    
    show_itemAvailedInPublicChat(room,user_data,item)
    
    
    

    return slot_machine_instance


def show_item_in_roomstats(room,user_data,item):
    channel_layer = get_channel_layer()
    channel_name = "broadcaster_visitor_" + str(room.User.id)
    print(channel_name,flush=True)
    
    # Prepare data to send
    data = {
        "user": user_data.User.username,
        "item": item.Item,
        "price": item.Cost,  # Changed "Cost" to "Price"
        "note": item.Note
    }
    
    # Send the data to the WebSocket consumer
    async_to_sync(channel_layer.group_send)(
        channel_name,
        {"type": "show.itemAvailed", "data": data}
    )


def show_itemAvailedInPublicChat(room,user_data,item):
    channel_layer = get_channel_layer()
    channel_name = "public_chat_" + room.User.username
    print(channel_name,flush=True)
    
    # Prepare data to send
    item = {
        "user": user_data.User.username,
        "item": item.Item,
        "price": item.Cost,  # Changed "Cost" to "Price"
        "note": item.Note
    }
    
    # Send the data to the WebSocket consumer
    async_to_sync(channel_layer.group_send)(
        channel_name,
        {"type": "show.itemAvailed", "item": item}
    )

def availed_item(user,room,item,price,game_type=None,random_button=None,button_cost=None,note=None):
    
    try:
        
        with transaction.atomic():
            user_data = User_Data.objects.get(User__id=user)
            
            if user_data.Free_spins != 0:
                
                item = Item_Availed.objects.create(Room=room,User=user_data.User,Item=item, Cost=0, Note="free spin")
                user_data.Availed.add(item)  
                
                slot_instance = display_user_availed_item_in_broadcaster_room(user_data,item,room,random_button,button_cost,remaining_price=price)
                
                
                remaining_price = privatevibez_chargeback(price,game_type)

                if room.Revenue != None:
                    room.Revenue += remaining_price
                else:
                    room.Revenue = remaining_price
                room.save()
            
                return slot_instance
                
            
            elif user_data.Vibez >= price:
                                
                remaining_price = privatevibez_chargeback(price,game_type)
                
                item = Item_Availed.objects.create(Room=room,User=user_data.User,Item=item, Cost=remaining_price, Note=note)
                user_data.Availed.add(item)
                    

                    
                
                slot_instance = display_user_availed_item_in_broadcaster_room(user_data,item,room,random_button,button_cost,remaining_price)

                # add revenues
                
           
                if room.Revenue != None:
                    room.Revenue += remaining_price
                else:
                    room.Revenue = remaining_price
                room.save()
                
                print(room.Revenue,flush=True)
                
                return slot_instance
                
            else:
                return JsonResponse({"data":f'Not enough vibez!'},status=500,safe=False)
        
    except IntegrityError as e:
        
        print(e,flush=True)

    

def fav_btn_trigger_toy(request):
    
    try:
    
        if request.method == "POST":
            
            with transaction.atomic():
                
                room_data = Room_Data.objects.get(User=request.POST.get('room_id'))
                user_id = request.POST.get('user_id')
                user_data = User_Data.objects.get(User=user_id)
                button_type = request.POST.get('button_type')
                
                if str(button_type) == "mmm":
                    
                    if user_data.Vibez < room_data.Price_MMM_button:
                        return JsonResponse(f'Not enough Vibez please buy.',status=500, safe=False)
                    
                    else:
                        user_vibez = fav_patterns_user_vibez_duduction(user_data,room_data,room_data.Price_MMM_button,"MMM")
                    
                    
                    broadcaster_id = room_data.User_id
                    price = room_data.Price_MMM_button
                
                    feature = room_data.Feature_MMM_button
                    strength = room_data.Strength_MMM_button
                    timesec = room_data.Duration_MMM_button

                    # Call the trigger_toy() function with the extracted attributes
                    trigger_toy(broadcaster_id, price, user_id, feature, strength, timesec)
                    
                if str(button_type) == "oh":
                    
                    if user_data.Vibez < room_data.Price_OH_button:
                        return JsonResponse(f'Not enough Vibez please buy.',status=500, safe=False)
                    
                    else:
                        user_vibez = fav_patterns_user_vibez_duduction(user_data,room_data,room_data.Price_OH_button,"OH")
                    
                    
                    broadcaster_id = room_data.User_id
                    price = room_data.Price_OH_button
            
                    feature = room_data.Feature_OH_button
                    strength = room_data.Strength_OH_button
                    timesec = room_data.Duration_OH_button

                    # Call the trigger_toy() function with the extracted attributes
                    trigger_toy(broadcaster_id, price, user_id, feature, strength, timesec)
                    
                if str(button_type) == "ohyes":
                    
                    if user_data.Vibez < room_data.Price_OHYes_button:
                        return JsonResponse(f'Not enough Vibez please buy.',status=500, safe=False)
                    else:
                        user_vibez = fav_patterns_user_vibez_duduction(user_data,room_data,room_data.Price_OHYes_button,"OHYes")
                        
                    availed_item(user_id,room_data,"OHYes",room_data.Price_OHYes_button)
                    
                    broadcaster_id = room_data.User_id
                    price = room_data.Price_OHYes_button
        
                    feature = room_data.Feature_OHYes_button
                    strength = room_data.Strength_OHYes_button
                    timesec = room_data.Duration_OHYes_button

                    # Call the trigger_toy() function with the extracted attributes
                    trigger_toy(broadcaster_id,price, user_id, feature, strength, timesec)
                
                return JsonResponse({'data': button_type + f' availed!','user_vibez':user_vibez},safe=False)
            
    except IntegrityError as e:
        
        print(e,flush=True)
        
        
def fav_patterns_user_vibez_duduction(user_data,room_data,button_cost,button_type):
    
    user_data.Vibez = user_data.Vibez - button_cost
    
    if room_data.Revenue != 0:
        room_data.Revenue += button_cost
    else:
        room_data.Revenue = button_cost
    
    room_data.save()
    
    item = Item_Availed.objects.create(Room=room_data,User=user_data.User,Item=button_type, Cost=button_cost, Note=button_type + " pattern")
    user_data.Availed.add(item)  
    
    user_data.save()
    
    show_item_in_roomstats(room_data,user_data,item)
    
    return user_data.Vibez

def get_invitees(request):
    
    
    try: 
        
        with transaction.atomic():
            if Private_Chat_Invitee.objects.filter(Broadcaster=request.user).exists():
                broadcaster = Private_Chat_Invitee.objects.get(Broadcaster=request.user)
                invitee_list = broadcaster.Invitee_relationships.all()
                
                invitees = []
                for invitee in invitee_list:
                    
                    if invitee.Is_Accepted == False:
                            invitees.append({
                                'user_id': invitee.Invitee.id,
                                'name'  : invitee.Invitee.username,
                            })
                    
                
                return JsonResponse({"data":invitees}, safe=False)
            else:
                return JsonResponse({"data":"None"}, safe=False)
            
    except IntegrityError as e:
        print(e,flush=True)
        
            
            
def accept_privatechat(request):
    
    if request.method == "POST":
        
        try:
            
            with transaction.atomic():
        
                user = User.objects.get(id = request.POST.get('user_id'))
            
                broadcaster = Private_Chat_Invitee.objects.get(Broadcaster=request.user, Invitee_relationships__Invitee=user)
                for invitee in broadcaster.Invitee_relationships.all():
                    if invitee.Invitee == user:
                        invitee.Is_Accepted = True
                        invitee.save()
                        print(invitee.Is_Accepted,flush=True)
                        
                        
                        channel_layer = get_channel_layer()
                        channel_name = "private_chat_invitation" + str(broadcaster.Broadcaster.username) + "_" +str(user.username)
                        print(channel_name,flush=True)
                            
                            # Prepare data to send
                        data = {
                            "is_invitation_accepted": True,
                        }
                        
                        # Send the data to the WebSocket consumer
                        async_to_sync(channel_layer.group_send)(
                            channel_name,
                            {"type": "is.InvitationAccepted", "data": data}
                        )
            
                
                return JsonResponse({'data':"success"}, safe=False)
        
        except IntegrityError as e:
            
            print(e,flush=True)
            
    
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
            region = Region.objects.filter(name_std__icontains=region)
            serializer = RegionSerializer(region, many=True)
            
            return JsonResponse({'data':serializer.data}, safe=False)
        else:
            return JsonResponse({'data':"none"}, safe=False)


def update_room_rules(request):
    
    
    if request.method == 'POST':
        
        try:
            
            with transaction.atomic():
                room_id = request.user
                room_instance = Room_Data.objects.get(User=room_id)
                rules = request.POST.get('room_rules')
                if rules is not None:
                    room_instance.Room_Rules = request.POST.get('room_rules')
                    room_instance.save()
            
                    return JsonResponse({"data":"Room rules updated"},safe=False)
                else:
                
                    return JsonResponse({"data":"Room rules is empty"}, safe=False)
        
        except IntegrityError as e:
            
            print(e,flush=True)
            
 
@csrf_exempt   
def update_room_description(request):
    
    
    if request.method == 'POST':
        
        try:
            
            with transaction.atomic():
                room_id = request.user
                room_instance = Room_Data.objects.get(User=room_id)
                description = request.POST.get('room_description')
                if description is not None:
                    room_instance.Room_Description = request.POST.get('room_description')
                    room_instance.save()
            
                    return JsonResponse({"data":"Room description updated"},safe=False)
                else:
                
                    return JsonResponse({"data":"Room description is empty"}, safe=False)
        
        except IntegrityError as e:
            
            print(e,flush=True)
            
    
    
def submit_bio(request):
    
    if request.method == 'POST':
        form = BioForm(request.POST,request.FILES)
        
        if form.is_valid():
            
            try:
                
                with transaction.atomic():
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
                        
                    print(form,flush=True)
                    return JsonResponse({'data':f'bio updated successfully!'}, safe=False)
                        
                    
            except IntegrityError as e:
                print(e,flush=True)
        else:
            print(form.errors,flush=True)
            return JsonResponse({'data':form.errors}, safe=False)


            
            
    

def save_hashtags(request):
    
    if request.method == "POST":
        hashtags = request.POST.get('hashtags')
        
        if hashtags is not None:
            
            try:
                
                room_data = Room_Data.objects.get(User=request.user)
                room_data.hashtags = hashtags
                room_data.save()
                
                return JsonResponse({'data':"Hashtags successfully saved!"}, safe=False)
            
            except Room_Data.DoesNotExist:
                return JsonResponse({'data':"Broadcaster does not exist"},status=500, safe=False)
            
            
            
        else:
            return JsonResponse({'data':"Hashtags is empty."}, safe=False)
        
     
     
def get_follower_spending(request,username,room):
    
    timestamp_str = request.GET.get('timestamp')
    print(timestamp_str, flush=True)

    print(username, flush=True)
    print(room, flush=True)
    if timestamp_str is None:
        item_availed = Item_Availed.objects.filter(
            User__username=username,
            Room__User__username=room,
            Timestamp__date=timezone.now().date()
        ).order_by('-Timestamp')

    else:

        # Convert the timestamp parameter to a datetime.date object
        timestamp_datetime = datetime.strptime(timestamp_str, '%Y-%m-%d')
        
        # Extract only the date part from the datetime object
        timestamp_date = timestamp_datetime.date()
        
        print(timestamp_date,flush=True)
        item_availed = Item_Availed.objects.filter(
            User__username=username,
            Room__User__username=room,
            Timestamp__date=timestamp_date
        ).order_by('-Timestamp')
        

 
        
    item_availed_serializer = Item_AvailedSerializer(item_availed,many=True)
        
    print(item_availed_serializer.data,flush=True)
    return JsonResponse({'data':item_availed_serializer.data},safe=False)
    
 
    
    
    
    
def get_user_by_date_spending(request):
    
    if request.method == 'GET':
        timestamp_str = request.GET.get('timestamp')
        timestamp_datetime = datetime.strptime(timestamp_str, '%Y-%m-%d')
        
        # Extract only the date part from the datetime object
        timestamp_date = timestamp_datetime.date()
        
        user_spendings = Item_Availed.objects.filter(User=request.user,Timestamp__date=timestamp_date)
        total_user_spendings = sum(int(item.Cost) for item in user_spendings)
        item_availed_serializer = Item_AvailedSerializer(user_spendings,many=True)

        return JsonResponse({"data": {"total_user_spendings": total_user_spendings,"user_spendings": item_availed_serializer.data}},safe=False)
    
    
def set_lottery_prize(request):
    
    if request.method == "POST":
        
        slot_values = []

        for i in range(0, 8):
            slot_name = f'slot{i}'
            slot_value = request.POST.get(slot_name)
            slot_values.append(slot_value)

            if Lottery.objects.filter(slot_number=i,User=request.user).exists():
                lottery = Lottery.objects.get(slot_number=i,User=request.user)
                
                if slot_value != "None":
                    lottery.prize = slot_value
                else:
                    lottery.prize = None
                
                lottery.save()
                
            else:
                
                if slot_value != "None":
                    lottery = Lottery.objects.create(slot_number=i,User=request.user,prize=slot_value)
        
        
        return JsonResponse({"data":f'lottery saved'},status=200, safe=False)
                
        

def set_dice_prize(request):
    
    if request.method == "POST":
        
        dice_values = []

        for i in range(1, 7):
            dice_name = f'dice{i}'
            dice_value = request.POST.get(dice_name)
            dice_values.append(dice_value)

            if Dice.objects.filter(dice_number=i,User=request.user).exists():
                dice = Dice.objects.get(dice_number=i,User=request.user)
                
                if dice_value != "None":
                    dice.prize = dice_value
                else:
                    dice.prize = None
                
                dice.save()
                
            else:
                
                if dice_value != "None":
                    dice = Dice.objects.create(dice_number=i,User=request.user,prize=dice_value)
        
        
        return JsonResponse({"data":f'lottery saved'},status=200, safe=False)
                
        



def get_lottery_prize(request):
    
    
    if request.method == "POST":
        
        winner = request.POST.get('winner')
        room = request.POST.get('room_name')
        lottery_number = request.POST.get('lottery_number')
        
        fav_btns_list = ['MMM','OH','OHYes']
        
        try:
            game_data = Games_Data.objects.order_by('-timestamp').first()
            user = User_Data.objects.get(User=request.user)
            print(room,flush=True)
            room_data = Room_Data.objects.get(User__username=room)
            if user.Vibez < game_data.Lottery_Spin_Cost:
                return JsonResponse({"data":f'not enough vibez!'},status=500, safe=False)

        except Games_Data.DoesNotExist:
            return JsonResponse({"data":f'there is some problem please contact staff'},status=500, safe=False)
        
        
        if Lottery.objects.filter(slot_number=lottery_number,User__username=room).exists():
            lottery_prize = Lottery.objects.get(slot_number=lottery_number,User__username=room)
            
            if lottery_prize.prize in fav_btns_list:
                
                if lottery_prize.prize == "MMM":
                    price = game_data.Lottery_Spin_Cost
                    feature = room_data.Feature_MMM_button
                    strength = room_data.Strength_MMM_button
                    timesec = room_data.Duration_MMM_button
                    
                    deduct_spin_or_vibez(user,room_data,price,game_type=None,game_data=None)
                    
                    note = f'Lottery win!'
                    availed_item(request.user.id,room_data,lottery_prize.prize,price,"Lottery",note)
                        
                    trigger_toy(room_data.User.id,price,request.user.id,feature,strength,timesec)
                    
                elif lottery_prize.prize == "OH":
                    price = game_data.Lottery_Spin_Cost
                    feature = room_data.Feature_OH_button
                    strength = room_data.Strength_OH_button
                    timesec = room_data.Duration_OH_button

                    deduct_spin_or_vibez(user,room_data,price,game_type=None,game_data=None)

                    note = f'Lottery win!'
                    availed_item(request.user.id,room_data,lottery_prize.prize,price,"Lottery",note)
                        
                    trigger_toy(room_data.User.id,price,request.user.id,feature,strength,timesec)
                    
                elif lottery_prize.prize == "OHYes":
                    price = game_data.Lottery_Spin_Cost
                    feature = room_data.Feature_OHYes_button
                    strength = room_data.Strength_OHYes_button
                    timesec = room_data.Duration_OHYes_button
                    
                    deduct_spin_or_vibez(user,room_data,price,game_type=None,game_data=None)

                    note = f'Lottery win!'
                    availed_item(request.user.id,room_data,lottery_prize.prize,price,"Lottery",note)
                        
                    trigger_toy(room_data.User.id,price,request.user.id,feature,strength,timesec)
            
            else:
                
                if Menu_Data.objects.filter(Menu_Name=lottery_prize,User__username=room).exists():
                    price = game_data.Lottery_Spin_Cost
                    menu_item = Menu_Data.objects.get(Menu_Name=lottery_prize,User__username=room)
                    item = Item_Availed.objects.create(Room = room_data,User=request.user, Item = menu_item.Menu_Name, Cost = menu_item.Vibez_Cost)
                    note = f'Lottery win!'
                    
                    user = User_Data.objects.get(User = request.user)
                    availed_item(request.user.id,room_data,lottery_prize.prize,menu_item.Vibez_Cost,"Lottery",note)
                    deduct_spin_or_vibez(user,room_data,price)
                    display_user_availed_item_in_broadcaster_room(user,item,room_data)
                    
                    show_item_in_roomstats(room_data,user,item)
            return JsonResponse({"data":f'you won {lottery_prize}',"spins":user.Free_spins,"vibez":user.Vibez},status=200, safe=False) 
        
        else:            
            price = game_data.Lottery_Spin_Cost
            remaining_price = privatevibez_chargeback(price,"Lottery")
            deduct_spin_or_vibez(user,room_data,remaining_price)
            
            if room_data.Revenue != None:
                room_data.Revenue += remaining_price
            else:
                room_data.Revenue = remaining_price
            
            if user.Free_spins != 0:
                cost = 0
            else:
                cost = price
                
            item = Item_Availed.objects.create(Room=room_data,User=user.User,Item="lottery loss", Cost=cost, Note="Lottery game")
            user.Availed.add(item) 
            
            show_item_in_roomstats(room_data,user,item)
            return JsonResponse({"data":f'it\'s okay to lose, try again!',"spins":user.Free_spins,"vibez":user.Vibez},status=500, safe=False) 


def privatevibez_chargeback(price,game_type):
        private_vibez = PrivatevibezRevenue.objects.order_by('timestamp').first()
        
        if private_vibez:
            # charge user per spin
            remaining_price = price - private_vibez.Chargeback
            print(remaining_price,flush=True)
            
            if game_type == "Slot_Machine":
                if private_vibez.Slot_Machine_Revenue is None:
                    private_vibez.Slot_Machine_Revenue = private_vibez.Chargeback
                else:
                    private_vibez.Slot_Machine_Revenue = private_vibez.Slot_Machine_Revenue + private_vibez.Chargeback
            
            elif game_type == "Lottery":
                if private_vibez.Lottery_Revenue is None:
                    private_vibez.Lottery_Revenue = private_vibez.Chargeback
                else:
                    private_vibez.Lottery_Revenue = private_vibez.Lottery_Revenue + private_vibez.Chargeback
                
                
            elif game_type == "Dice":
                if private_vibez.Dice_Revenue is None:
                    private_vibez.Dice_Revenue = private_vibez.Chargeback
                else:
                    private_vibez.Dice_Revenue = private_vibez.Dice_Revenue + private_vibez.Chargeback
                
            private_vibez.save()
            
            return remaining_price

def deduct_spin_or_vibez(user,broadcaster_room,price,game_type=None,game_data=None):
    
    print(price,flush=True)
    if user.Free_spins != 0:
        user.Free_spins -= 1
    else:
        if user.Vibez >= price:
            user.Vibez = user.Vibez - price
            

            

    user.save()
    broadcaster_room.save()
    
    

def enable_menu_items(request):
    
    if request.method == "POST":
        
        is_enabled = request.POST.get("is_enabled")
        
            
        room_data = Room_Data.objects.get(User=request.user)
        
        if room_data.Is_Menu_Active == True:
            room_data.Is_Menu_Active = False
        else:
            room_data.Is_Menu_Active = True
    
        
        room_data.save()
        update_games_accessibility(room_data)
        
        return JsonResponse({"data":f'Menu Items updated',"is_active":room_data.Is_Menu_Active},status=200,safe=True)
    

def enable_dice(request):
    if request.method == "POST":
        
        is_enabled = request.POST.get("is_enabled")
        
        room_data = Room_Data.objects.get(User=request.user)
        
        if room_data.Is_Dice_Active == True:
            room_data.Is_Dice_Active = False
        else:
            room_data.Is_Dice_Active = True
    
        
        
        room_data.save()
        update_games_accessibility(room_data)
        
        return JsonResponse({"data":f'Menu Items updated',"is_active":room_data.Is_Dice_Active},status=200,safe=True)
    
def update_games_accessibility(roomData):
    
    channel_layer = get_channel_layer()
    channel_name = "game_socket_" + str(roomData.User.id)
    print(channel_name,flush=True)
        
        # Prepare data to send
    data = {
        "is_Lottery_Active": roomData.Is_Lottery_Active,
        "is_Menu_Active": roomData.Is_Menu_Active,
        "is_Dice_Active": roomData.Is_Dice_Active
    }
    
    # Send the data to the WebSocket consumer
    async_to_sync(channel_layer.group_send)(
        channel_name,
        {"type": "updateGames", "data": data}
    )

def enable_lottery(request):
    
    if request.method == "POST":
        
        is_enabled = request.POST.get("is_enabled")
        
        room_data = Room_Data.objects.get(User=request.user)
        
        if room_data.Is_Lottery_Active == True:
            room_data.Is_Lottery_Active = False
        else:
            room_data.Is_Lottery_Active = True
    
        
        room_data.save()
        update_games_accessibility(room_data)
        
        return JsonResponse({"data":f'Menu Items updated',"is_active":room_data.Is_Lottery_Active},status=200,safe=True)
    
    
    
def give_dice_price(request):
    
    
    if request.method == "POST":
        
        
        fav_btns_list = ['MMM','OH','OHYes']
        
        try:
            room = request.POST.get('room')
            
            game_data = Games_Data.objects.order_by('-timestamp').first()
            dice_number = int(request.POST.get('dice_number'))
            user = User_Data.objects.get(User=request.user)
        
            room_data = Room_Data.objects.get(User__username=room)
            
            if user.Vibez < game_data.Dice_Spin_Cost:
                return JsonResponse({"data":f'not enough vibez!'},status=500, safe=False)

        except Games_Data.DoesNotExist:
            return JsonResponse({"data":f'there is some problem please contact staff'},status=500, safe=False)
        
        
        if Dice.objects.filter(dice_number=dice_number,User__username=room).exists():
            dice_prize = Dice.objects.get(dice_number=dice_number,User__username=room)
            
            if dice_prize.prize in fav_btns_list:
                
                if dice_prize.prize == "MMM":
                    price = game_data.Dice_Spin_Cost
                    feature = room_data.Feature_MMM_button
                    strength = room_data.Strength_MMM_button
                    timesec = room_data.Duration_MMM_button
                    
                    deduct_spin_or_vibez(user,room_data,price,game_type=None,game_data=None)
                    
                    note = f'Dice win!'
                    availed_item(request.user.id,room_data,dice_prize.prize,price,"Dice",note)
                        
                    trigger_toy(room_data.User.id,price,request.user.id,feature,strength,timesec)
                    
                elif dice_prize.prize == "OH":
                    price = game_data.Dice_Spin_Cost
                    feature = room_data.Feature_OH_button
                    strength = room_data.Strength_OH_button
                    timesec = room_data.Duration_OH_button

                    deduct_spin_or_vibez(user,room_data,price,game_type=None,game_data=None)

                    note = f'Dice win!'
                    availed_item(request.user.id,room_data,dice_prize.prize,price,"Dice",note)
                        
                    trigger_toy(room_data.User.id,price,request.user.id,feature,strength,timesec)
                    
                elif dice_prize.prize == "OHYes":
                    price = game_data.Dice_Spin_Cost
                    feature = room_data.Feature_OHYes_button
                    strength = room_data.Strength_OHYes_button
                    timesec = room_data.Duration_OHYes_button
                    
                    deduct_spin_or_vibez(user,room_data,price,game_type=None,game_data=None)

                    note = f'Dice win!'
                    availed_item(request.user.id,room_data,dice_prize.prize,price,"Dice",note)
                        
                    trigger_toy(room_data.User.id,price,request.user.id,feature,strength,timesec)
            
            else:
                
                if Menu_Data.objects.filter(Menu_Name=dice_prize,User__username=room).exists():
                    price = game_data.Dice_Spin_Cost
                    menu_item = Menu_Data.objects.get(Menu_Name=dice_prize,User__username=room)
                    item = Item_Availed.objects.create(Room = room_data,User=request.user, Item = menu_item.Menu_Name, Cost = menu_item.Vibez_Cost)
                    note = f'Dice win!'
                    
                    user = User_Data.objects.get(User = request.user)
                    availed_item(request.user.id,room_data,dice_prize.prize,menu_item.Vibez_Cost,"Dice",note)
                    deduct_spin_or_vibez(user,room_data,price)
                    display_user_availed_item_in_broadcaster_room(user,item,room_data)
                        
            return JsonResponse({"data":f'you won {dice_prize}',"spins":user.Free_spins,"vibez":user.Vibez},status=200, safe=False) 
        
        else:            
            price = game_data.Dice_Spin_Cost
            remaining_price = privatevibez_chargeback(price,"Dice")
            deduct_spin_or_vibez(user,room_data,remaining_price)
            
            if room_data.Revenue != None:
                room_data.Revenue += remaining_price
            else:
                room_data.Revenue = remaining_price

            room_data.save()
            
            if user.Free_spins != 0:
                cost = 0
            else:
                cost = price
                
            item = Item_Availed.objects.create(Room=room_data,User=user.User,Item="dice loss", Cost=cost, Note="Dice game")
            user.Availed.add(item) 
            
            show_item_in_roomstats(room_data,user,item)

            return JsonResponse({"data":f'it\'s okay to lose, try again!',"spins":user.Free_spins,"vibez":user.Vibez},status=500, safe=False) 
