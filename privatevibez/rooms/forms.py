from django.forms import ModelForm
from .models import Slot_Machine, Room_Data
from django import forms

class Slot_MachineForm(ModelForm):
  
  class Meta:
    
    model = Slot_Machine
    exclude = ('User',)
    fields = ['User','pot']
    
    
class Fav_vibezForm(ModelForm):
  
  class Meta:
    
    model = Room_Data
    fields = [
      'Price_MMM_button',
      'Price_OH_button',
      'Price_OHYes_button',
      'Duration_MMM_button',
      'Duration_OH_button',
      'Duration_OHYes_button',
      'Strength_MMM_button',
      'Strength_OH_button',
      'Strength_OHYes_button',
              ]
    
    
class BioForm(forms.Form):
    
    goal_vibez =forms.IntegerField(label='Goal Vibez',required=True)
    username = forms.CharField(label='Username',required=True)
    real_name = forms.CharField(label='Real Name',required=True)
    I_am = forms.CharField(label='I am',required=True)
    Interested_In = forms.CharField(label='Interested In',required=True)
    Location = forms.CharField(label='Locations',required=True)
    Language = forms.CharField(label='Language',required=True)
    Body_Type = forms.CharField(label='Body Type',required=True)
    profile_pic = forms.ImageField(label='Profile Pic',required=False)
    
    

class MenuDataForm(forms.Form):
  
    menu_item = forms.CharField(label='Item=',required=True)
    menu_item_price = forms.IntegerField(label='Price=',required=True)
    menu_item_duration = forms.IntegerField(label='Duration=',required=True)
    
    

class SocialMediaLinks(forms.Form):
    instagram_link = forms.CharField(label='Instagram Link',required=False)
    onlyfans_link = forms.CharField(label='Onlyfans Link',required=False)
    snapchat_link = forms.CharField(label='Snapchat Link',required=False)
    amazon_link = forms.CharField(label='Amazon Link',required=False)
    
    instagram_vibez_cost = forms.IntegerField(label='Instagram Vibez Cost',required=False)
    onlyfans_vibez_cost = forms.IntegerField(label='Onlyfans Vibez Cost',required=False)
    snapchat_vibez_cost = forms.IntegerField(label='Snapchat Vibez Cost',required=False)
    amazon_vibez_cost = forms.IntegerField(label='Amazon Vibez Cost',required=False)