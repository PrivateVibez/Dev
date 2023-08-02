from rest_framework import serializers
from staff.models import StaffRoomManager
from chat.models import Staff
from accounts.models import User_Data
from django.contrib.auth import get_user_model
User = get_user_model()


class StaffRoomManagerSerializer(serializers.ModelSerializer):
    Staff = serializers.StringRelatedField()
    
    class Meta:
        
        model = StaffRoomManager
        fields =['Staff']
        
class StaffMessagesSerializer(serializers.ModelSerializer):
    From = serializers.StringRelatedField()
    To = serializers.StringRelatedField()
    
    class Meta:
        
        model = Staff
        fields =['From','To','Message','Timestamp']
        
        
class UserStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = User_Data
        fields =['User','Timestamp','Real_Name','Image','Id_File','Birth_Date','Age']