# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room_Data, Room_Visitors
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
User = get_user_model()


class UserVisitorsConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
    
        self.room_group_name = 'broadcaster_visitor_%s' % (self.room_id)

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
    
    
    def add_visitor_to_room(self,room,visitor):
        room = room
        room_instance = room.Visitors.add(visitor)
        
    @database_sync_to_async
    def get_all_visitors(self):
        room_data = Room_Data.objects.get(User=self.room_id)
        visitors = room_data.Visitors.all() 

        dic = {}
        for v in visitors:
            dic[v.pk] = {
                'id': v.User.id,
                'username': v.User.username,
            }
        return dic
        
    @database_sync_to_async
    def get_room_instance(self):
        room_data = Room_Data.objects.get(User_id=self.room_id)
       
        return room_data

    @database_sync_to_async
    def create_room_visitor(self, user_id):
        
        if Room_Visitors.objects.filter(User_id=user_id).exists():
            room_id = Room_Visitors.objects.get(User_id=user_id)
        else:
            room_id = Room_Visitors.objects.create(User_id=user_id)
       
        return room_id
   
   
    async def send_user_visitors(self, data):
        await self.send(text_data=json.dumps(data))

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action', None)
        
        if action == 'retrieve_visitors':
            await self.broadcast_user_visitors()

        user_id = data.get('user_id', None)
        is_leaving = data.get('leaving', False)
        
        room_instance = await self.get_room_instance()
        


        if is_leaving:
            if user_id is not None:
                room_visitor = await self.create_room_visitor(user_id)
                await database_sync_to_async(room_instance.Visitors.remove)(room_visitor)
        else:
            if user_id is not None:
                room_visitor = await self.create_room_visitor(user_id)
                await database_sync_to_async(self.add_visitor_to_room)(room_instance, room_visitor)

        user_visitors = [str(visitor) for visitor in await self.get_all_visitors()]
        await self.send_user_visitors({'user_visitors': user_visitors})
        
    
    async def broadcast_user_visitors(self):
        room_instance = await self.get_room_instance()
        visitors =  await self.get_all_visitors()
        await self.send(text_data=json.dumps({'user_visitors': visitors}))
        
        
        
        
class BlockedCountriesConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
    
        self.room_group_name = 'blocked_countries_%s' % (self.room_id)

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
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action', None)
        
        await self.send(text_data=json.dumps({'user_visitors': visitors}))
