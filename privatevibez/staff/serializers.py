from rest_framework import serializers
from staff.models import StaffRoomManager, StaffManager
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
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  # Include User fields you need

        
        
class UserStatusSerializer(serializers.ModelSerializer):
    
    user_id = serializers.IntegerField(source='User.id', read_only=True)
    username = serializers.CharField(source='User.username', read_only=True)
    first_name = serializers.CharField(source='User.first_name', read_only=True)
    last_name = serializers.CharField(source='User.last_name', read_only=True)
    email = serializers.EmailField(source='User.email', read_only=True)
    
    class Meta:
        
        model = User_Data
        fields =['user_id','username','first_name','last_name','email','Timestamp','Real_Name','Image','Id_File','Birth_Date','Age']
        
        
        

class StaffSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = StaffManager
        fields = ['staff_id','email','fname','lname','address','profile_pic','birthday']