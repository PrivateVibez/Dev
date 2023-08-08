from chat.models import Private_Chat_Invitee
from rest_framework import serializers
from cities_light.models import Country, Region


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