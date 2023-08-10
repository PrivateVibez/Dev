from django.forms import ModelForm
from .models import Slot_Machine, Room_Data
from django import forms

class Slot_MachineForm(ModelForm):
  
  class Meta:
    
    model = Slot_Machine
    exclude = ('User',)
    fields = ['User','Slot_cost_per_spin','Win_3_of_a_kind_prize','Win_2_of_a_kind_prize']
    
    
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
    
    
    