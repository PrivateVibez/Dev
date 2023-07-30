from django.db import models
from django_softdelete.models import SoftDeleteModel
from django.conf import settings


# Create your models here.
class Public(SoftDeleteModel):
    User      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Room      = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True, on_delete=models.CASCADE, related_name = 'Messages_room')
    Message   = models.CharField(max_length=20)
    Timestamp = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.User)

class Private(SoftDeleteModel):
    From       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    To         = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True, on_delete=models.CASCADE, related_name = 'To_Message')
    Message    = models.CharField(max_length=20)
    Timestamp  = models.DateTimeField(auto_now_add=True)
    sent_by_fan = models.BooleanField(default=False, null=True)

    def __str__(self):
        return str(self.From)
    
class Private_Chat_Invitee(SoftDeleteModel):
    broadcaster     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Invitee         = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, symmetrical=False, related_name="invitee")

    def __str__(self):
        return str(self.broadcaster.username)  
    
class Staff(SoftDeleteModel):
    From       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'Staff_From_Message')
    To         = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True, on_delete=models.CASCADE, related_name = 'Staff_To_Message')
    Message    = models.CharField(max_length=20)
    Timestamp  = models.DateTimeField(auto_now_add=True)
    sent_by_fan = models.BooleanField(default=False, null=True)

    def __str__(self):
        return str(self.From)

class PrivateRoomManager(models.Model):
    broadcaster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fan_list = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True, symmetrical=False, related_name="fans")

    def add_fan(self, user):
        self.fan_list.add(user)
        self.save()

    def remove_fan(self, user):
        self.fan_list.remove(user)
        self.save()

    def total_fans(self):
        return self.fan_list.count()

    def __str__(self):
        return self.broadcaster.username