from rest_framework import serializers
from .models import User_Data
from rooms.models import Room_Data
from django.contrib.auth import get_user_model
User = get_user_model()

class User_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Data
        fields = ['id','Real_Name','Image']  # You can specify specific fields if needed
        
class Room_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room_Data
        fields = ['id','Tab']  # You can specify specific fields if needed
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']  # You can specify specific fields if needed
        
        
        
class UserDataSubscriptionSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='User.username')
    subscription = serializers.ReadOnlyField(source='Subscription_Type.Name')
    badge = serializers.ReadOnlyField(source='Subscription_Type.Badge.url')
    
    

    class Meta:
        
        model = User_Data
        fields = ['username','subscription','Free_spins','Vibez','badge']