from django.db import models
from rooms.models import Room_Data
from django.contrib.auth.models import AbstractUser

from django.conf import settings

class CustomUser(AbstractUser):
    # Add new fields here
    Is_Accepted_Invite = models.BooleanField(default=False, blank=True)
    Is_Sent_Invite = models.BooleanField(default=False, blank=True)
    Status     = models.CharField(max_length=20, null=True, blank=True, default="User")
    Decline_Message = models.CharField(max_length=250, null=True, blank=True)
    Ip_Address = models.CharField(max_length=250, null=True, blank=True)
    Ip_Address_Expires = models.DateTimeField(null=True, blank=True) 
    Country = models.CharField(max_length=250, null=True, blank=True)
    Region = models.CharField(max_length=250, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True, blank=True)
    # ... add more fields as needed

    def __str__(self):
        return self.username
    
class User_Status(models.Model):
    User       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Status     = models.CharField(max_length=20)
    Timestamp  = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.User)

class Subscription(models.Model):
    Name       = models.CharField(max_length=200, null=True, blank=True)
    Cost       = models.CharField(max_length=200, null=True, blank=True)
    Vibez      = models.IntegerField(null=True,blank=True,default=0)
    Slots      = models.IntegerField(null=True,blank=True,default=0)
    Badge      = models.ImageField(upload_to='subscription_badge',null=True,blank=True)
    Timestamp  = models.DateTimeField(auto_now_add=True, null=True, blank=True)     
    def __str__(self):
        return str(self.Name)

class User_Data(models.Model):
    User           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Birth_Date     = models.CharField(null=True,blank=True, max_length=500)
    Real_Name      = models.CharField(max_length=200,null=True,blank=True)
    Age            = models.IntegerField(null=True,blank=True)
    I_Am           = models.CharField(max_length=200,null=True,blank=True)
    Interested_In  = models.CharField(max_length=200,null=True,blank=True)
    Location       = models.CharField(max_length=200,null=True,blank=True)
    Language       = models.CharField(max_length=200,null=True,blank=True)
    Body_Type      = models.CharField(max_length=200,null=True,blank=True)
    Vibez          = models.IntegerField(null=True,blank=True,default=0)
    U_token        = models.CharField(max_length=200,null=True,blank=True)
    Image          = models.ImageField(upload_to='profile_pic',null=True,blank=True)
    Id_File        = models.ImageField(upload_to='ID',null=True,blank=True)
    Second_Id_File = models.ImageField(upload_to='2nd_ID',null=True,blank=True)
    Availed        = models.ManyToManyField('Item_Availed',related_name='Item_Avail',blank=True)
    Subscription_Type =  models.ForeignKey(Subscription, on_delete=models.CASCADE,null=True, blank=True)
    Free_spins     = models.IntegerField(null=True,blank=True,default=0)
    Timestamp      = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.User)


class Bad_Acters(models.Model):
    Reporty    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Reported   = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True, on_delete=models.CASCADE, related_name = 'reported')
    Message    = models.CharField(null=True,blank=True, max_length=500)
    Staff      = models.CharField(null=True,blank=True, max_length=500)
    Timestamp  = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.Reporty)
    
class Memos(models.Model):
    From    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Memos_from")
    To      = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True, on_delete=models.CASCADE, related_name = 'Memos_To')
    Message    = models.CharField(null=True,blank=True, max_length=500)
    Timestamp  = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.Message)


class Item_Availed(models.Model):
    Room = models.ForeignKey(Room_Data, related_name="Broadcaster",on_delete=models.CASCADE, null=True, blank=True)
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,blank=True)
    Item = models.CharField(max_length=200,null=True,blank=True)
    Cost = models.CharField(max_length=200,null=True,blank=True)
    Note = models.TextField(null=True,blank=True)
    Timestamp  = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.Item)
    
    



