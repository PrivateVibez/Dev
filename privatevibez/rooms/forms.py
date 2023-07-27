from django.forms import ModelForm
from .models import Slot_Machine


class Slot_MachineForm(ModelForm):
  
  class Meta:
    
    model = Slot_Machine
    fields = ['User','Slot_cost_per_spin','Win_3_of_a_kind_prize','Win_2_of_a_kind_prize']