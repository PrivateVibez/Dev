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
    username = forms.CharField(widget=forms.TextInput(attrs={'style': 'font-size:2rem;'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'style': 'font-size:2rem;'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'style': 'font-size:2rem;'}))


    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        
class BioInfoForm(forms.Form):
    promotion_code = forms.CharField(widget=forms.TextInput(attrs={'style': 'font-size:2rem;'}))
    Real_Name      = forms.CharField(widget=forms.TextInput(attrs={'style': 'font-size:2rem;'}))
    Age            = forms.IntegerField(widget=forms.TextInput(attrs={'style': 'font-size:2rem;'}))
    I_Am           = forms.CharField(widget=forms.TextInput(attrs={'style': 'font-size:2rem;'}))
    Interested_In  = forms.CharField(widget=forms.TextInput(attrs={'style': 'font-size:2rem;'}))
    Location       = forms.CharField(widget=forms.TextInput(attrs={'style': 'font-size:2rem;'}))
    Language       = forms.CharField(widget=forms.TextInput(attrs={'style': 'font-size:2rem;'}))
    Body_Type      = forms.CharField(widget=forms.TextInput(attrs={'style': 'font-size:2rem;'}))
    Tab            = forms.CharField(widget=forms.TextInput(attrs={'style': 'font-size:2rem;'}))
        





class UserFnLnameForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
    

class CustomPasswordChangeForm(PasswordChangeForm):
    # Add any additional fields or customization here, if needed
    pass



class ChangePasswordForm(forms.Form):
  
  password1 = forms.CharField(label='Password',required=True)
  password2 = forms.CharField(label='Password',required=True)
    


class ChangeEmailForm(forms.Form):
    
    email = forms.EmailField(label='Email',required=True)
    

class BroadcasterRegistrationForm(forms.Form):
    
    cropped_image = forms.ImageField(label='Cropped Image',required=True)
    first_Name = forms.CharField(label='First Name',required=True)
    last_Name = forms.CharField(label='Last Name',required=True)
    birth_Date = forms.DateField(label='Birth Date',required=True)
    id_Picture = forms.ImageField(label='Id Picture',required=True)
    Real_Name = forms.CharField(label='Real Name',required=True)
    Age = forms.IntegerField(label='Age',required=True)
    I_Am = forms.CharField(label='I Am',required=True)
    Tab  = forms.CharField(label='Tab',required=True)
    Interested_In = forms.CharField(label='Interested In',required=True)
    Location = forms.CharField(label='Location',required=True)
    Language = forms.CharField(label='Language',required=True)
    Body_Type = forms.CharField(label='Body Type',required=True)
    

