from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
from staff.models import StaffRoomManager
import json
from staff.serializers import StaffRoomManagerSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse as httpresponse
from django.conf import settings
from .models import Private_Chat_Invitee
from django.contrib.auth import get_user_model
User = get_user_model()


def get_last_10_messages(chatId):
    chat = get_object_or_404(Public, id=chatId)
    return chat.Message.order_by('-Timestamp').all()[:10]

def fan_list(request, broc):
    try:
        broadcaster = User.objects.get(username=broc)
        private_room_manager = Private_Chat_Invitee.objects.get(Broadcaster=broadcaster)
        
        return JsonResponse({'data': fan_list})
    except:
        return JsonResponse({'data': []})
    
def staff_list(request, broc):

    staff = User.objects.get(username=broc,is_staff=True)

    staff_room_manager = StaffRoomManager.objects.get(Staff=staff.id)
    staff_list = StaffRoomManager.objects.all()
    serializer = StaffRoomManagerSerializer(staff_list, many=True) 
    
    return JsonResponse(serializer.data, safe=False)
