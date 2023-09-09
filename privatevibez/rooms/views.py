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
from staff.models import PrivatevibezRevenue
from django.utils.safestring import mark_safe
import json
import random
from .forms import Slot_MachineForm, Fav_vibezForm, BioForm, MenuDataForm
from django.http import HttpResponse as httpresponse
import requests
from .decorators import check_user_blocked_ip,check_user_status
from accounts.forms import CustomPasswordChangeForm
from cryptography.fernet import Fernet
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .serializers import Private_Chat_InviteeSerializer, CountrySerializer, RegionSerializer, SlotMachineSerializer
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
                            user_datas        = User_Data.objects.get(User =  request.user)
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
                            availed_items = Item_Availed.objects.filter(Room = room_data).all()
                    
                        
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
                                    slot_machine_cost_per_spin = Slot_Machine_Data.objects.order_by('-timestamp').values('Slot_Machine_Spin_Cost').first()
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
                                    
                                    
                                    print(availed_items,flush=True)
                                    if Private_Chat_Invitee.objects.filter(Broadcaster=request.user).exists():
                                        private_chat_invite = Private_Chat_Invitee.objects.get(Broadcaster=request.user)
                                        pending_private_chat_invitees = private_chat_invite.Invitee_relationships.filter(Is_Accepted=False).count()
                                        all_private_chat_invitees = private_chat_invite.Invitee_relationships.all()
                                        
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
                
                print("existing", flush=True)
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
    elif random_button == "OH":
        feature = room_data.Feature_OH_button
        strength = room_data.Strength_OH_button
        timesec = room_data.Duration_OH_button
    elif random_button == "MMM":
        feature = room_data.Feature_MMM_button
        strength = room_data.Strength_MMM_button
        timesec = room_data.Duration_MMM_button
        
    return feature, strength, timesec
    
    
@csrf_exempt
def get_prize(request):
    
    if request.method == 'POST':
        
            try:
                
                try:
                    with transaction.atomic():
                        winner = User_Data.objects.get(User__id=request.POST.get('winner'))
                        broadcaster = request.POST.get('broadcaster')
                        prize = request.POST.get('prize_won')
                        cost_per_spin = int(request.POST.get('cost_per_spin'))
                        room_data = get_object_or_404(Room_Data, User_id=broadcaster)     
                
                except IntegrityError as e:
                    print(e,flush=True)
                    
                    
            except User_Data.DoesNotExist as e:
                return JsonResponse({'data':f'Broadcaster does not exist'},status=500, safe=False)
           
           
            if winner.Vibez >= cost_per_spin or winner.Free_spins != 0:
                if prize == "2OAK":
                    
                    feature, strength, timesec = random_favorite_button(room_data)
                    price = cost_per_spin
                    
                    note = f'{winner.User.username} Won Two of a kind!'
            
                    pot = availed_item(winner.User.id,room_data,"2OAK",price,note)
                    
                    winner = trigger_toy(room_data.User.id,price,winner.User.id,feature,strength,timesec)
                    
                    msg = f'Two of a kind!!'
                    data = player_remaining_spins_or_vibez(winner,msg,pot)
                    
                    
                if prize == "3OAK":
                    feature = room_data.Feature_OHYes_button
                    strength = room_data.Strength_OHYes_button
                    timesec = room_data.Duration_OHYes_button
                    price = cost_per_spin
                    note = f'{winner.User.username} Won Three of a kind!'
            
                    pot = availed_item(winner.User.id,room_data,"3OAK",price,note)
                    
                    is_Jackpot = True
                    winner = trigger_toy(room_data.User.id,price,winner.User.id,feature,strength,timesec,room_data,is_Jackpot)
                    
                    msg = f'JACPOT!!!!!'
                    data = player_remaining_spins_or_vibez(winner,msg,pot)
                
                if prize == "Loss":
                    feature = room_data.Feature_OH_button
                    strength = room_data.Strength_OH_button
                    timesec = 1    
                    print("costperspin",flush=True)
                    print(cost_per_spin,flush=True)
                    if winner.Free_spins != 0:
                        remaining_price = cost_per_spin
                    else:
                        remaining_price = charge_user(cost_per_spin)
                    
                    

                    availed_item(winner.User.id,room_data,"Slot Spin",remaining_price,"Loss")
                    winner = trigger_toy(room_data.User.id,cost_per_spin,winner.User.id,feature,strength,timesec)
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
                            room_data.Revenue += broadcaster_private_chat_price
                            room_data.save()
                            broadcaster.Invitee_relationships.add(invitee_relationship)
                            
                            channel_layer = get_channel_layer()
                            channel_name = "private_chat_invitation" + str(broadcaster.Broadcaster.username) + "_" + str(user.User.username)
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
                try:
                    with transaction.atomic():
                        player = User_Data.objects.get(User__id=user_id)
                        
                        if player.Free_spins != 0:
                            player.Free_spins -= 1
                            player.save()
                            
                            return player
                        else:
                            
                            player.Vibez = player.Vibez - price
                            player.save()
                            return player
                
                except IntegrityError as e:
                    
                    print(e,flush=True)
                
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
                try:
                    with transaction.atomic():
                        player = User_Data.objects.get(User__id=user_id)
                        
                        if player.Free_spins != 0:
                            player.Free_spins -= 1
                            player.save()
                            
                            return player
                        else:
                            
                            player.Vibez = player.Vibez - price
                            player.save()
                            return player
                
                except IntegrityError as e:
                    
                    print(e,flush=True)
                
                return JsonResponse({'data': response_data},safe=False)
            else:

                return JsonResponse({"error": "Failed to make the POST request."}, status=response.status_code)

        except requests.exceptions.RequestException as e:  
            return JsonResponse({"error": str(e)}, status=500) 
        
  


def display_user_availed_item_in_broadcaster_room(user_data,item,room,remaining_price=None):
    # Get the channel layer
  
    if item.Item == "3OAK":
        print(item,flush=True)
        slot_machine = Slot_Machine.objects.filter(User=room.User).first()
        if slot_machine:
            # Retrieve values from the Slot_Machine object
            
            
            pot = slot_machine.pot
            
                
            # Calculate the new revenue value
            new_revenue = room.Revenue + pot 
                
            # Update the room's revenue
            if room.Revenue is not None:
                room.Revenue = new_revenue - remaining_price
                room.save()
            else:
                print('room error',flush=True)
            
                
                
             # Make sure to save the room object

            # Update the Slot_Machine object's pot_increase
            slot_machine.pot = remaining_price
            slot_machine.save()
            
            slot_machine_instance = slot_machine.pot
            
    else:
        slot_machine_instance = None
    
    
    show_itemAvailedInPublicChat(room,user_data,item)
    
    
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

    return slot_machine_instance


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

def availed_item(user,room,item,price,note=None):
    
    try:
        
        with transaction.atomic():
            user_data = User_Data.objects.get(User__id=user)
            
            if user_data.Free_spins != 0:
                item = Item_Availed.objects.create(Room=room,User=user_data.User,Item=item, Cost=0, Note="free spin")
                user_data.Availed.add(item)  
                
                slot_instance = display_user_availed_item_in_broadcaster_room(user_data,item,room,remaining_price=price)
                
                
                return slot_instance
                
                
            if user_data.Vibez >= price:
                
                private_vibez = PrivatevibezRevenue.objects.order_by('timestamp').first()
                
                if private_vibez:
                    # charge user per spin
                    remaining_price = price - private_vibez.Chargeback
                    print(remaining_price,flush=True)
                    if private_vibez.Slot_Machine_Revenue is None:
                        private_vibez.Slot_Machine_Revenue = private_vibez.Chargeback
                    else:
                        private_vibez.Slot_Machine_Revenue = private_vibez.Slot_Machine_Revenue + private_vibez.Chargeback
                    private_vibez.save()
                
                
                item = Item_Availed.objects.create(Room=room,User=user_data.User,Item=item, Cost=remaining_price, Note=note)
                user_data.Availed.add(item)
                    

                    
                
                slot_instance = display_user_availed_item_in_broadcaster_room(user_data,item,room,remaining_price)

                # add revenues
           
                if room.Revenue is not None:
                    room.Revenue = room.Revenue + remaining_price
                else:
                    room.Revenue = remaining_price
                room.save()
                
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
                    
                    availed_item(user_id,room_data,"MMM",room_data.Price_MMM_button)
                    
                    
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
                    
                    
                    availed_item(user_id,room_data,"OH",room_data.Price_OH_button)
                    
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
                    
                            
                    availed_item(user_id,room_data,"OHYes",room_data.Price_OHYes_button)
                    
                    broadcaster_id = room_data.User_id
                    price = room_data.Price_OHYes_button
        
                    feature = room_data.Feature_OHYes_button
                    strength = room_data.Strength_OHYes_button
                    timesec = room_data.Duration_OHYes_button

                    # Call the trigger_toy() function with the extracted attributes
                    trigger_toy(broadcaster_id,price, user_id, feature, strength, timesec)
                
                return JsonResponse({'data': button_type + f' availed!'},safe=False)
            
    except IntegrityError as e:
        
        print(e,flush=True)
        


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
                        channel_name = "private_chat_invitation" + str(broadcaster.Broadcaster.username) + "_" + str(user.username)
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
            region = Region.objects.filter(display_name__icontains=region)
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
        
     