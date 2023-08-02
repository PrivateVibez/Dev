from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User_Data
from django.contrib.auth import get_user_model
User = get_user_model()

class Profile_Image(forms.ModelForm):

    class Meta:
        model = User_Data
        fields = ['Image']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    Status = forms.CharField(max_length=100, widget=forms.HiddenInput(),  initial="User")
    class Meta:
        model = User
        fields = ['username',  'Status',  'email', 'password1', 'password2']



class UserFnLnameForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


