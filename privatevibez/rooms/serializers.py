from chat.models import Private_Chat_Invitee
from rest_framework import serializers



class Private_Chat_InviteeSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Private_Chat_Invitee
        fields = '__all__'