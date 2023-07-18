from channels.generic.websocket import AsyncWebsocketConsumer
import json


class StaffConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "staff"
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

    async def user_update(self, event):
        data = {
        "pending": json.loads(event['data'])["pending"],
        "user_data": json.loads(event['data'])["user_data"],
        }
        await self.send(text_data=json.dumps(data))


class BadActersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "bad_acters"
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

    async def acter_update(self, event):
        data = json.loads(event['data'])
        await self.send(text_data=json.dumps(data))