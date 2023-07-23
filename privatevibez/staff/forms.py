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
        fields = ['username', 'email', 'is_staff', 'password1', 'password2']
        
        
class AddStaffPermission(forms.Form):

    email = forms.EmailField()
    permissions = forms.MultipleChoiceField(
        choices=[('can_add_staff', 'Can add staff'), ('can_edit_staff', 'Can edit staff'), ('can_delete_staff', 'Can delete staff'),
        ("can_view_staff", "Can view a staff"),
        ("can_view_dashboard", "Can view a dashboard"),
        ("can_view_id_check", "Can view a ID Check"),
        ("can_view_bad_acters", "Can view a bad acters"),
        ("can_view_todo_list", "Can view a todo list"),
         ("can_view_inbox", "Can view a inbox"),
        ]
    )
    
    
class AddStaff(forms.ModelForm):
    class Meta:
        
        model = StaffManager
        fields = ['fname', 'lname', 'birthday', 'address', 'id_photo', 'profile_pic']
        




