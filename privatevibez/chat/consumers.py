from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
import json
from .models import Public, Private, PrivateRoomManager, Staff
from staff.models import StaffRoomManager
from django.db.models import Q
import time
from django.contrib.auth import get_user_model
User = get_user_model()


class PublicChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'public_chat_%s' % (self.room_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
        
        
    # show user availed item in broadcaster public chat
    
    async def show_itemAvailed(self,event):
        item = event['item']
        modified_data = {
        "item_availed": item
            }
        await self.send(text_data=json.dumps(modified_data))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        user, created = await sync_to_async(User.objects.get_or_create)(username=username)
        room, created = await sync_to_async(User.objects.get_or_create)(username=self.room_name)
        await sync_to_async(Public.objects.get_or_create)(User=user, Room=room, Message=message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

        
class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.broc = self.scope['url_route']['kwargs']['broc']
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.room_group_name = 'private_chat_%s_%s' % (self.broc, self.user_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        user = await sync_to_async(User.objects.get)(username=username)
        to_user = await sync_to_async(User.objects.get)(username=self.broc)
        created_data = await sync_to_async(Private.objects.create)(From=user, To=to_user, Message=message, sent_by_fan=True)
        fan_list, created = await sync_to_async(PrivateRoomManager.objects.get_or_create)(broadcaster=to_user)
        await sync_to_async(fan_list.add_fan)(user)
        if created_data.sent_by_fan:
            self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'private_chat_message',
                    'message': message,
                    'username': username
                }
            )
        else:
            self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'private_chat_message',
                        'message': message,
                        'username': created_data.To
                    }
                )
            

    # Receive message from room group
    async def private_chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
    async def private_chat_message_broc(self, event):
        b_from = event['from']
        to = event['to']
        message = event['message']
        sent_by = event['sent_by']
        if sent_by:
            await self.send(text_data=json.dumps({
                'message': message,
                'username': b_from
            }))
        else:
            await self.send(text_data=json.dumps({
                'message': message,
                'username': to
            }))


class PrivateChatConsumerBroc(JsonWebsocketConsumer):
    # Keep track of last submission time for each user
    last_submission_time = {}

    def connect(self):
        self.broc = self.scope['url_route']['kwargs']['broc']
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.room_group_name = 'private_chat_broc_%s_%s' % (self.broc, self.user_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "room_join_data",
                "broc": self.broc,
                "user": self.user_name
            }
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        current_time = time.time()

        # Check if there was a submission from this user within the last 3 seconds
        if self.user_name in self.last_submission_time and (current_time - self.last_submission_time[self.user_name] < 0.5):
            print("multiple submissions within 0.5 seconds are not allowed")
            return

        # Update the last submission time for this user
        self.last_submission_time[self.user_name] = current_time
        broc = User.objects.get(username=self.broc)
        user = User.objects.get(username=self.user_name)
        Private.objects.create(From=broc, To=user, Message=message, sent_by_fan=False)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "broc": self.broc,
                "user": self.user_name
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # send joining data of specific user and broc
    def room_join_data(self, event):
        broc = User.objects.get(username=event['broc'])
        user = User.objects.get(username=event['user'])
        data = Private.objects.filter(
            Q(From=user, To=broc) | Q(To=user, From=broc)
        ).order_by('Timestamp')
        data = [{
        "From": obj.From.username,
        "To": obj.To.username,
        "Message": obj.Message,
        "Timestamp": obj.Timestamp.strftime("%d-%m-%Y %H:%M"),
        "sent_by": obj.sent_by_fan
    } for obj in data]
        self.send(text_data=json.dumps({
            'data': data
        }))

    def chat_message(self, event):
        broc = User.objects.get(username=event['broc'])
        user = User.objects.get(username=event['user'])
        data = Private.objects.filter(
            Q(From=user, To=broc) | Q(To=user, From=broc)
        ).order_by('Timestamp')
        
        data = [{
        "From": obj.From.username,
        "To": obj.To.username,
        "Message": obj.Message,
        "Timestamp": obj.Timestamp.strftime("%d-%m-%Y %H:%M"),
        "sent_by": obj.sent_by_fan
    } for obj in data]
        self.send(text_data=json.dumps({
            'data': data
        }))
        
        
        
        # CONSUMER FOR STAFF CHAT
        
class StaffChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.broc = self.scope['url_route']['kwargs']['broc']
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.room_group_name = 'staff_chat_%s_%s' % (self.broc, self.user_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        user = await sync_to_async(User.objects.get)(username=username)
        to_user = await sync_to_async(User.objects.get)(username=self.broc)
        created_data = await sync_to_async(Staff.objects.create)(From=user, To=to_user, Message=message)
        staff_list, created = await sync_to_async(StaffRoomManager.objects.get_or_create)(broadcaster=to_user)

 
        self.channel_layer.group_send(
            self.room_group_name,
                {
                    'type': 'staff_chat_message',
                    'message': message,
                    'username': created_data.To
                }
            )
        

    # Receive message from room group
    async def staff_chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
    async def staff_chat_message_broc(self, event):
        b_from = event['from']
        to = event['to']
        message = event['message']
        sent_by = event['sent_by']
        if sent_by:
            await self.send(text_data=json.dumps({
                'message': message,
                'username': b_from
            }))
        else:
            await self.send(text_data=json.dumps({
                'message': message,
                'username': to
            }))


class StaffChatConsumerBroc(JsonWebsocketConsumer):
    # Keep track of last submission time for each user
    last_submission_time = {}

    def connect(self):
        self.broc = self.scope['url_route']['kwargs']['broc']
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.room_group_name = 'staff_chat_broc_%s_%s' % (self.broc, self.user_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "room_join_data",
                "broc": self.broc,
                "user": self.user_name
            }
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        current_time = time.time()

        # Check if there was a submission from this user within the last 3 seconds
        if self.user_name in self.last_submission_time and (current_time - self.last_submission_time[self.user_name] < 0.5):
            print("multiple submissions within 0.5 seconds are not allowed")
            return

        # Update the last submission time for this user
        self.last_submission_time[self.user_name] = current_time
        broc = User.objects.get(username=self.broc)
        user = User.objects.get(username=self.user_name)
        Staff.objects.create(From=broc, To=user, Message=message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "broc": self.broc,
                "user": self.user_name
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # send joining data of specific user and broc
    def room_join_data(self, event):
        broc = User.objects.get(username=event['broc'])
        user = User.objects.get(username=event['user'])
        data = Staff.objects.filter(From=broc, To=user)
        data = [{
        "From": obj.From.username,
        "To": obj.To.username,
        "Message": obj.Message,
        "Timestamp": obj.Timestamp.strftime("%d-%m-%Y %H:%M"),
        "sent_by": obj.From.username
    } for obj in data]
        self.send(text_data=json.dumps({
            'data': data
        }))

    def chat_message(self, event):
        broc = User.objects.get(username=event['broc'])
        user = User.objects.get(username=event['user'])
        data = Staff.objects.filter(From=broc, To=user)
        data = [{
        "From": obj.From.username,
        "To": obj.To.username,
        "Message": obj.Message,
        "Timestamp": obj.Timestamp.strftime("%d-%m-%Y %H:%M"),
        "sent_by": obj.From.username    
    } for obj in data]
        self.send(text_data=json.dumps({
            'data': data
        }))