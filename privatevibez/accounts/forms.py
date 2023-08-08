from django import forms

from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from accounts.models import User_Data
from django.contrib.auth import get_user_model
User = get_user_model()

class Profile_Image(forms.ModelForm):

    class Meta:
        model = User_Data
        fields = ['Image']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class UserFnLnameForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
    

class CustomPasswordChangeForm(PasswordChangeForm):
    # Add any additional fields or customization here, if needed
    pass


