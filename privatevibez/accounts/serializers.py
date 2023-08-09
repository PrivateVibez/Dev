from rest_framework import serializers
from .models import User_Data
from rooms.models import Room_Data
from django.contrib.auth import get_user_model
User = get_user_model()

class User_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Data
        fields = '__all__'  # You can specify specific fields if needed
        
class Room_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room_Data
        fields = '__all__'  # You can specify specific fields if needed
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # You can specify specific fields if needed