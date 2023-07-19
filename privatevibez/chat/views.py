from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
from staff.models import StaffRoomManager
import json

User = get_user_model()

def get_last_10_messages(chatId):
    chat = get_object_or_404(Public, id=chatId)
    return chat.Message.order_by('-Timestamp').all()[:10]

def fan_list(request, broc):
    try:
        broadcaster = User.objects.get(username=broc)
        private_room_manager = PrivateRoomManager.objects.get(broadcaster=broadcaster)
        fan_list = private_room_manager.fan_list.values('username')
        return JsonResponse({'data': list(fan_list)})
    except:
        return JsonResponse({'data': []})
    
def staff_list(request, broc):
    try:
        staff = User.objects.get(username=broc,is_staff=True)
        staff_room_manager = StaffRoomManager.objects.get(Staff=staff)
        staff_list = StaffRoomManager.objects.all()
        print(staff_room_manager)
        return JsonResponse({'data': list(staff_list)})
    except:
        return JsonResponse({'data': []})