from django.forms import ModelForm
from .models import Slot_Machine, Room_Data


class Slot_MachineForm(ModelForm):
  
  class Meta:
    
    model = Slot_Machine
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