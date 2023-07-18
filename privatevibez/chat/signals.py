from django.dispatch import receiver
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Private

@receiver(post_save, sender=Private)
def private_post_save(sender, instance, created, **kwargs):
    if created:
            channel_layer = get_channel_layer()
            broc = str(instance.To.username)
            user = str(instance.From.username)
            message = str(instance.Message)
            room_group_name = 'private_chat_%s_%s' % (broc, user)
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    "type": "private_chat_message_broc",
                    "from": user,
                    "to": broc,
                    "message": message,
                    "sent_by": instance.sent_by_fan
                }
            )
            room_group_name_broc = 'private_chat_broc_%s_%s' % (broc, user)
            async_to_sync(channel_layer.group_send)(
                room_group_name_broc,
                {
                    "type": "chat_message",
                    "broc": broc,
                    "user": user
                }
            )