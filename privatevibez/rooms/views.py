from django.shortcuts import render
from django.contrib.auth.models import User
from rooms.models import *
from accounts.models import *
from chat.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from django.utils.safestring import mark_safe
import json

# Create your views here.
def Room(request, Broadcaster):
    if Broadcaster == str(request.user):
        is_broadcaster = True
    else:
        is_broadcaster = False        
    
    print(request.user)
    print(Broadcaster)
    rooms                = Room_Data.objects.all()
    room_users_data      = User_Data.objects.all()    
    broadcaster_status   = User_Status.objects.get(User = User.objects.get(username = Broadcaster))
    room_data            = Room_Data.objects.get(User = User.objects.get(username = Broadcaster))
    # room_sesson          = Room_Sesson.objects.get(User = User.objects.get(username = Broadcaster))
    broadcaster_data     = User_Data.objects.get(User = User.objects.get(username = Broadcaster))
    if request.user.is_authenticated:
        user_data        = User_Data.objects.get(User =  request.user)
        user_status_data = User_Status.objects.get(User = request.user)
        user_status      = user_status_data.Status
        broadcaster_user     = User.objects.get(username = Broadcaster)
        room_name_json       = mark_safe(json.dumps(broadcaster_user.username))
        room_name            = broadcaster_user.username
        username             = mark_safe(json.dumps(request.user.username))
        try:
            broc_manager = PrivateRoomManager.objects.get(broadcaster=broadcaster_user)
            broc_private_list = broc_manager.fan_list.all()
        except PrivateRoomManager.DoesNotExist:
            broc_private_list = []
        private_chat         = Private.objects.filter(From=request.user, To=broadcaster_user)
        public_chat          = Public.objects.filter(Room = User.objects.get(username=Broadcaster)).all
        follows              = Follows.objects.filter(User = request.user).all
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

    else:
            user_data   = None
            user_status = None
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
    room.save()
    return JsonResponse('OK', safe=False)