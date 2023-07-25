from rest_framework import serializers
from staff.models import StaffRoomManager, StaffManager


class StaffRoomManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffRoomManager
        fields = ['Staff']