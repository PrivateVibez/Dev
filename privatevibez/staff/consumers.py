from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from accounts.models import User_Data
from django.contrib.auth import get_user_model
User = get_user_model()


class PrivateVibezRevenueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "privatevibezrevenue"
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
        
        
    async def show_updatedRevenue(self,event):
        data = event['data'];
        print(data,flush=True)

        await self.send(text_data=json.dumps(data))
    



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
        
        
    async def showPending_Broadcaster(self,event):
        data = event['data'];
        print(data,flush=True)
        modified_data = {
        "user_data": data
            }
        await self.send(text_data=json.dumps(modified_data))
        

    @sync_to_async
    def get_pending_broadcasters(self,status):
        return list(User_Data.objects.all().filter(User__Status=status))

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        status = data.get('Status')
        user_id = data.get('user_id')

        # Wrap the synchronous database update operation in sync_to_async
        await sync_to_async(User.objects.filter(id=user_id).update)(Status=status)
 

        # Wrap the synchronous database query operation in sync_to_async
        pending_broadcasters = await self.get_pending_broadcasters("Pending_Broadcaster")

        # Prepare the data to be sent back to the socket
        data = [
            {
                "id": user.id,
                "name": user.Real_Name,
                "image": user.Image.url if user.Image else "",
                "Birth_Date": user.Birth_Date,
                # Add any other user fields you want to send back
            }
            for user in pending_broadcasters
        ]

        # Send the updated data back to the socket
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