from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import serializers
from accounts.models import *
from chat.models import Staff
import json

channel_layer = get_channel_layer()

@receiver(post_save, sender=User_Data)
def send_update_to_consumer(sender, instance, **kwargs):
    pending = User_Status.objects.filter(Status='Pending_Broadcaster')
    pending_queryset = list(User_Status.objects.filter(Status='Pending_Broadcaster').values())
    pending_user_id = list(pending.values_list('User__id',flat=True))
    user_data = list(User_Data.objects.filter(User__id__in=pending_user_id).values('id', 'Birth_Date', 'Id_File', 'User__id', 'User__first_name', 'User__last_name'))
    data = json.dumps({
        "pending": json.dumps(pending_queryset, cls=DjangoJSONEncoder),
        "user_data": json.dumps(user_data, cls=DjangoJSONEncoder),
    })
    async_to_sync(channel_layer.group_send)('staff', {'type': 'showPending.Broadcaster', 'data': data})


@receiver(post_save, sender=User_Status)
def send_update_to_consumer(sender, instance, **kwargs):
    pending = User_Status.objects.filter(Status='Pending_Broadcaster')
    pending_queryset = list(User_Status.objects.filter(Status='Pending_Broadcaster').values())
    pending_user_id = list(pending.values_list('User__id',flat=True))
    user_data = list(User_Data.objects.filter(User__id__in=pending_user_id).values('id', 'Birth_Date', 'Id_File', 'User__id', 'User__first_name', 'User__last_name'))
    data = json.dumps({
        "pending": json.dumps(pending_queryset, cls=DjangoJSONEncoder),
        "user_data": json.dumps(user_data, cls=DjangoJSONEncoder),
    })
    async_to_sync(channel_layer.group_send)('staff', {'type': 'showPending.Broadcaster', 'data': data})


@receiver(post_save, sender=Bad_Acters)
def send_bad_acters_to_consumer(sender, instance, **kwargs):
    bad_acters = Bad_Acters.objects.all().values('id', 'Reporty__username', 'Reported__username', 'Message')
    data = json.dumps(list(bad_acters), cls=DjangoJSONEncoder)
    async_to_sync(channel_layer.group_send)('bad_acters', {'type': 'acter_update', 'data': data})
    
    
    
    

@receiver(post_save, sender=Staff)
def staff_post_save(sender, instance, created, **kwargs):
    if created:
            channel_layer = get_channel_layer()
            broc = str(instance.To.username)
            user = str(instance.From.username)
            message = str(instance.Message)
            room_group_name = 'staff_chat_%s_%s' % (broc, user)
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    "type": "staff_chat_message_broc",
                    "from": user,
                    "to": broc,
                    "message": message,
                    "sent_by": instance.From_id
                }
            )
            room_group_name_broc = 'staff_chat_broc_%s_%s' % (broc, user)
            async_to_sync(channel_layer.group_send)(
                room_group_name_broc,
                {
                    "type": "chat_message",
                    "broc": broc,
                    "user": user
                }
            )