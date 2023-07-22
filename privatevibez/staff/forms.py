from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User_Data
from .models import StaffManager



class Profile_Image(forms.ModelForm):

    class Meta:
        model = User_Data
        fields = ['Image']


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'is_staff', 'password1', 'password2']
        
        
class AddStaffPermission(forms.Form):

    email = forms.EmailField()
    permissions = forms.MultipleChoiceField(
        choices=[('can_add_staff', 'Can add staff'), ('can_edit_staff', 'Can edit staff'), ('can_delete_staff', 'Can delete staff')]
    )
    
    
class AddStaff(forms.ModelForm):
    class Meta:
        
        model = StaffManager
        fields = ['fname', 'lname', 'birthday', 'address', 'id_photo', 'profile_pic']
        




