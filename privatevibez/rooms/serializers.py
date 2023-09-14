from chat.models import Private_Chat_Invitee
from rest_framework import serializers
from cities_light.models import Country, Region
from .models import Slot_Machine, Room_Data
from accounts.models import Item_Availed
from django.contrib.auth import get_user_model
User = get_user_model()


class Private_Chat_InviteeSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Private_Chat_Invitee
        fields = '__all__'
        
        
class CountrySerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Country
        fields = ['name']
        
class RegionSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Region
        fields = ['display_name']
        
        
class SlotMachineSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Slot_Machine
        fields = ['pot']
        
     
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username']
             
      
      
class RoomSerializer(serializers.ModelSerializer):
     User = UserSerializer()
     
     class Meta:
          model = Room_Data
          fields = ['User']  

class Item_AvailedSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='User.username', read_only=True)

    class Meta:
        model = Item_Availed
        fields = ['Item', 'Cost', 'Note', 'username', 'Timestamp']
