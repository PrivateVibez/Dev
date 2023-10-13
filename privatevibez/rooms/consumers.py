# consumers.py

import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room_Data, Room_Visitors,  Blocked_Countries, Blocked_Regions, Room_Viewer
from cities.models import City, Country, Region
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
User = get_user_model()

class FollowingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
    
        self.room_group_name = 'following_%s' % (self.room_id)

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
        
    async def broadcaster_followers(self, event):
        data = event['data']
        modified_data = {
        "followers": data
            }
        await self.send(text_data=json.dumps(modified_data))
 

class TestBroadacasterFavButtonConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
    
        self.room_group_name = 'update_fav_button_visibility'

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
        
    async def updateFavButtonVisibility(self, event):
        data = event['data']
        modified_data = {
        "is_fav_button_visible": data
            }
        print("showing",flush=True)
        await self.send(text_data=json.dumps(modified_data))
        
        
        
class GamesListOfPrizesConsumer(AsyncWebsocketConsumer):   
    
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
    
        self.room_group_name = 'update_games_list_%s' % (self.room_id)

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
        
    async def updateGameListOfPrizes(self, event):
        data = event['data']
        modified_data = {
            "is_updated": True,

        }
        print(modified_data,flush=True)
        await self.send(text_data=json.dumps(modified_data))
        
        
        

class GamesSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
    
        self.room_group_name = 'game_socket_%s' % (self.room_id)

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
        
    async def updateGames(self, event):
        data = event['data']
        modified_data = {
            "is_Lottery_Active": data['is_Lottery_Active'],
            "is_Menu_Active": data['is_Menu_Active'],
            "is_Dice_Active": data['is_Dice_Active']
        }
        print(modified_data,flush=True)
        await self.send(text_data=json.dumps(modified_data))
        
        

class RoomViewersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
    
        self.room_group_name = 'room_viewers_%s' % (self.room_id)

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
     
        modified_data = {
        "saved": True
            }
        await self.send(text_data=json.dumps(modified_data))
        
    
    async def show_visitors(self, event):
        
        data = event['data']
        
        await self.send(text_data=json.dumps(data))
        
    

class UserSessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_group_name = 'user_session'

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
        
    
    async def logoutuser(self, event):
        data = event['data']
        modified_data = {
        "is_user_logged_out": data
            }
        await self.send(text_data=json.dumps(modified_data))
           
    
    
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
        
    
    # Display availed items in broadcaster room
    async def show_itemAvailed(self, event):
        data = event['data']
        modified_data = {
        "item_availed": data
            }
        await self.send(text_data=json.dumps(modified_data))
        
        
        
    def remove_visitor_from_room(self,room,visitor):
        room = room
        room_instance = room.Visitors.remove(visitor)
        
        print(room.Visitors.all(),flush=True)
        
        channel_layer = get_channel_layer()
        channel_name = "room_viewers_" + str(self.room_id)
        
            
            # Prepare data to send
        data = {
            "is_leaving": True,
        }
        
        # Send the data to the WebSocket consumer
        async_to_sync(channel_layer.group_send)(
            channel_name,
            {"type":"show.visitors","data": data},
        )
        
        self.send(text_data=json.dumps({'is_leaving': True}))
    
    
    def add_visitor_to_room(self,room,visitor):
        room = room
        room_instance = room.Visitors.add(visitor)
        
        print(room.Visitors.all(),flush=True)
        
        if room.Viewers.filter(User__id=visitor.User.id).exists():
            pass
        else:
            room_viewer = Room_Viewer.objects.create(User=visitor.User)
            
            if room.Total_Viewers is not None:
                room.Total_Viewers += 1
                
            else:
                room.Total_Viewers = 1
            
            room.save()
            
            room.Viewers.add(room_viewer)
            
            
        
        channel_layer = get_channel_layer()
        channel_name = "room_viewers_" + str(self.room_id)
        
            
            # Prepare data to send
        data = {
            "is_leaving": False,
        }
        
        # Send the data to the WebSocket consumer
        async_to_sync(channel_layer.group_send)(
            channel_name,
            {"type":"show.visitors","data": data},
        )
        
        self.send(text_data=json.dumps({'is_leaving': False}))
        
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
    def get_or_create_room_visitor(self, user_id):
        
        if Room_Visitors.objects.filter(User_id=user_id).exists():
            room_id = Room_Visitors.objects.get(User_id=user_id)
        else:
            room_id = Room_Visitors.objects.create(User_id=user_id)
       
        return room_id
   
   

    async def receive(self, text_data):
        
        data = json.loads(text_data)
        action = data.get('action', None)
        
        if action == 'retrieve_visitors':
            await self.broadcast_user_visitors()

        if action == 'bought_item':
            await self.show_bought_item()
            
        user_id = data.get('user_id', None)
        is_leaving = data.get('leaving', False)
        
        room_instance = await self.get_room_instance()
        
        
        print(is_leaving,flush=True)
        print(self.room_group_name,flush=True)

        if is_leaving:
            if user_id is not None:
                room_visitor = await self.get_or_create_room_visitor(user_id)
                await database_sync_to_async(self.remove_visitor_from_room)(room_instance, room_visitor)
                
                
        else:
            if user_id is not None:
                room_visitor = await self.get_or_create_room_visitor(user_id)
                await database_sync_to_async(self.add_visitor_to_room)(room_instance, room_visitor)

    
    
    async def send_user_visitors(self, data):
        try:
            print(data,flush=True)
            await self.send(text_data=json.dumps(data))
        except Exception as e:
            print(f"Error during send: {e}", flush=True)

    async def broadcast_user_visitors(self):
        room_instance = await self.get_room_instance()
        visitors =  await self.get_all_visitors()
        await self.send(text_data=json.dumps({'user_visitors': visitors}))
        
        
        
        
class BlockedCountriesConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
    
        self.room_group_name = 'blocking_places_%s' % (self.room_id)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
            
    
    @database_sync_to_async
    def block_countries(self,country):
        room_data = Room_Data.objects.get(User_id=self.room_id)
                
        try:
            country_instance = Country.objects.get(name=country)
            blocking_instance, created = Blocked_Countries.objects.get_or_create(Country=country_instance)
            
            try:

                room_data.Blocked_Countries.add(blocking_instance)
                blocked_countries = room_data.Blocked_Countries.all()
                self.send_blocked_countries({'blocked_countries': blocked_countries})
            except Room_Data.DoesNotExist:
                
                pass
        except Country.DoesNotExist:
            pass
        
    
    @database_sync_to_async
    def block_regions(self,region):
            room_data = Room_Data.objects.get(User_id=self.room_id)
            try:
                region_instance = Region.objects.get(name=region)
                blocking_instance, created = Blocked_Regions.objects.get_or_create(Region=region_instance)

                try:

                    room_data.Blocked_Regions.add(blocking_instance)
                    blocked_regions = room_data.Blocked_Regions.all()
                    self.send_blocked_regions({'blocked_regions': blocked_regions})
                except Room_Data.DoesNotExist:
                    
                    pass
            except Region.DoesNotExist:
                pass
            
            pass
     
    @database_sync_to_async
    def remove_country(self,country):
            room_data = Room_Data.objects.get(User_id=self.room_id)
            try:
                country_instance = Country.objects.get(name=country)
                blocking_instance = Blocked_Countries.objects.get(Country=country_instance)
                
                try:
                    room_data.Blocked_Countries.remove(blocking_instance)
                except Room_Data.DoesNotExist:
                    
                    pass
            except Country.DoesNotExist:
                pass
            
            pass
    
     
    @database_sync_to_async
    def remove_region(self,region):
            room_data = Room_Data.objects.get(User_id=self.room_id)
            try:
                region_instance = Region.objects.get(name_std=region)
                blocking_instance = Blocked_Regions.objects.get(Region=region_instance)
                
                try:
                    room_data.Blocked_Regions.remove(blocking_instance)
                except Room_Data.DoesNotExist:
                    
                    pass
            except Country.DoesNotExist:
                pass
        
            pass
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_blocked_countries(self, data):
        await self.send(text_data=json.dumps(data))
        
        
    async def send_blocked_regions(self, data):
        await self.send(text_data=json.dumps(data))

    

    async def add_block(self,action, country, region):

        if action is not None and action == "block_countries":
            await self.block_countries(country)
        
        if action is not None and action == "block_regions":
            await self.block_regions(region)


    
    async def remove_block(self, action,country,region):
        
        if action is not None and action == "able_countries":
        
            await self.remove_country(country)

        
        if action is not None and action == "able_regions":
            await self.remove_region(region)
            
            
    async def receive(self, text_data):
        data = json.loads(text_data)

        method = data.get('type')
        action = data.get('action', None)
        country = data.get('country', None)
        region = data.get('region', None)
        
  
        if method == "add_block":
  
            await self.add_block(action,country,region)
        if method == "remove_block":
            await self.remove_block(action,country,region)
    
