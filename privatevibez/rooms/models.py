from django.db import models
from django.conf import settings
from cities_light.models import Country, Region
# Create your models here.

class Blocked_Countries(models.Model):
    Country    = models.ForeignKey(Country, on_delete=models.CASCADE, null=True,blank=True)
    Timestamp  = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.Country)
    
    
class Blocked_Regions(models.Model):
    Region     = models.ForeignKey(Region, on_delete=models.CASCADE, null=True,blank=True)
    Timestamp  = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.Region)

class Block_Ip_Address(models.Model):

    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Room_Visitors(models.Model):
    User       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,blank=True)
    Timestamp  = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.User)
 
    
class Room_Data(models.Model):
    User                  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Tab                   = models.CharField(max_length=200,null=True,blank=True)
    Goal                  = models.IntegerField(null=True,blank=True, default=0)
    Public_Chat           = models.BooleanField(default=True)
    Private_Chat          = models.BooleanField(default=True)
    Private_Chat_Price    = models.IntegerField(null=True,blank=True, default=0)
    Price_MMM_button      = models.IntegerField(null=True,blank=True, default=10)
    Price_OH_button       = models.IntegerField(null=True,blank=True, default=50)
    Price_OHYes_button    = models.IntegerField(null=True,blank=True, default=75)
    Duration_MMM_button   = models.IntegerField(null=True,blank=True, default=1)
    Duration_OH_button    = models.IntegerField(null=True,blank=True, default=2)
    Duration_OHYes_button = models.IntegerField(null=True,blank=True, default=3)
    
    Strength_MMM_button   = models.CharField(null=True,blank=True, max_length=100)
    Strength_OH_button    = models.CharField(null=True,blank=True, max_length=100)
    Strength_OHYes_button = models.CharField(null=True,blank=True, max_length=100)
    
    Feature_OHYes_button = models.CharField(max_length=1,null=True,blank=True)
    Feature_OH_button = models.CharField(max_length=1,null=True,blank=True)
    Feature_MMM_button = models.CharField(max_length=1,null=True,blank=True)
    Visitors              = models.ManyToManyField(Room_Visitors, null=True, blank=True)
    Is_Active             = models.BooleanField(default=False)
    Blocked_Countries       = models.ManyToManyField(Blocked_Countries, related_name='block_countries', blank=True)
    Blocked_Regions       = models.ManyToManyField(Blocked_Regions, related_name='block_regions', blank=True)
    Room_Rules            = models.TextField(null=True,blank=True)
    Timestamp             = models.DateTimeField(auto_now_add=True)     
    
    def __str__(self):
        return str(self.User)

class Room_Sesson(models.Model):
    User           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Goal_Currrent  = models.IntegerField(null=True,blank=True, default=0)
    Timestamp      = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.User)


class Menu_Data(models.Model):
    User       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Vibez_Cost = models.IntegerField(null=True,blank=True)
    Menu_Name  = models.CharField(max_length=200,null=True,blank=True)
    Menu_Time  = models.CharField(max_length=200,null=True,blank=True)
    Timestamp  = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.User)

class Dice_Data(models.Model):
    User             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    One_Dice_Name    = models.CharField(max_length=200,null=True,blank=True)
    One_Dice_Time    = models.IntegerField(null=True,blank=True)
    Two_Dice_Name    = models.CharField(max_length=200,null=True,blank=True)
    Two_Dice_Time    = models.IntegerField(null=True,blank=True)
    Three_Dice_Name  = models.CharField(max_length=200,null=True,blank=True)
    Three_Dice_Time  = models.IntegerField(null=True,blank=True)
    Four_Dice_Name   = models.CharField(max_length=200,null=True,blank=True)
    Four_Dice_Time   = models.IntegerField(null=True,blank=True)
    Five_Dice_Name   = models.CharField(max_length=200,null=True,blank=True)
    Five_Dice_Time   = models.IntegerField(null=True,blank=True)
    Six_Dice_Name    = models.CharField(max_length=200,null=True,blank=True)
    Six_Dice_Time    = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return str(self.User)
   
   
class Slot_Machine_limit(models.Model):
    
    Number_of_Three_of_a_kind_winners     = models.IntegerField(null=True, blank=True)
    Number_of_Two_of_a_kind_winners       = models.IntegerField(null=True, blank=True)
    Number_of_Three_of_a_kind_losers      = models.IntegerField(null=True, blank=True)
    Number_of_Two_of_a_kind_losers        = models.IntegerField(null=True, blank=True)
    Timestamp                   = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.Three_of_a_kind_winners)
    
    

class Slot_Machine(models.Model):
    User                      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Slot_cost_per_spin        = models.IntegerField(null=True,blank=True)
    Win_3_of_a_kind_prize     = models.CharField(max_length=200,null=True,blank=True)
    Win_2_of_a_kind_prize     = models.CharField(max_length=200,null=True,blank=True)
    Prize                     = models.CharField(max_length=200,null=True,blank=True)
    Winner                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True, related_name = 'Winner')
    timestamp                 = models.DateTimeField(null=True)
    
    def __str__(self):
        return str(self.User)
    
    
    
    

class Follows(models.Model):
    User        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Broacaster  = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True, on_delete=models.CASCADE, related_name = 'Broacaster')
    Timestamp   = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.User)



class Thumbs(models.Model):
    User        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Broacaster  = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True, on_delete=models.CASCADE, related_name = 'Thumb_Broacaster')
    Thumb       = models.CharField(max_length=200,null=True,blank=True)
    Timestamp   = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.User)


