# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room_Data, Room_Visitors

from channels.db import database_sync_to_async


class UserVisitorsConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_room_instance(self):
        return Room_Data.objects.get(User_id=self.room_id)

    @database_sync_to_async
    def create_room_visitor(self, user_id):
        return Room_Visitors.objects.create(User_id=user_id)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_id = data['user_id']
        is_leaving = data.get('leaving', False)

        room_instance = await self.get_room_instance()

        if is_leaving:
            room_visitor = await self.create_room_visitor(user_id)
            room_instance.Visitors.remove(room_visitor)
        else:
            room_visitor = await self.create_room_visitor(user_id)
            room_instance.Visitors.add(room_visitor)

        user_visitors = [str(visitor) for visitor in room_instance.Visitors.all()]
        await self.send_user_visitors({'user_visitors': user_visitors})
