from rest_framework import serializers
from staff.models import StaffRoomManager
from chat.models import Staff


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