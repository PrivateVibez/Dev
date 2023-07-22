from django.shortcuts import render
from django.contrib.auth.models import User, Group, Permission
from accounts.models import *
from rooms.models import *
from staff.models import *
from django.conf import settings
from .forms import UserRegisterForm, AddStaffPermission, AddStaff
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.backends.base import SessionBase
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import redirect
from .forms import UserRegisterForm
from django.contrib.contenttypes.models import ContentType




# Create your views here.

def home(request):

        
        pending = User_Status.objects.filter(Status='Pending_Broadcaster')
        pending_user_id = list(pending.values_list('User__id',flat=True))
        user_data = User_Data.objects.filter(User__id__in=pending_user_id)
        users_status = User_Status.objects.all()
        users_data = User_Data.objects.all()
        bad_acters = Bad_Acters.objects.all()
        to_do_projects_dev = ToDoProject_Dev.objects.all()
        to_do_lists_Dev = ToDolist_Dev.objects.all()
        to_do_lists_Dev_count = to_do_lists_Dev.count
        
        # staff chat
        try:
            broc_manager = StaffRoomManager.objects.get(Staff=request.user)
            room_name            = User.objects.get(username=request.user)
            print(room_name)
            broc_staff_list = StaffRoomManager.objects.all()
        #     print(broc_staff_list)
        except StaffRoomManager.DoesNotExist:
            broc_staff_list = []
        
        

        # Get a list of dictionaries with session information for all users
        sessions_info = []
        all_sessions = Session.objects.all()
        # all_sessions = all_sessions.session_data
        
        
        for session in all_sessions:
 
                session = Session.objects.get(pk=session)
                session_data = session.get_decoded()
                user_id = session_data.get('_auth_user_id')
                print(user_id)
  
                user = User.objects.get(pk=user_id)
                is_session_active = session.expire_date > timezone.now()
                
                sessions_info.append({
                        'user': user.username,
                        'session_expire': session.expire_date,
                        'is_session_active': is_session_active,
                }),
        
        print(sessions_info)
        
        
        return render(request, "staff/home.html", locals())
        
@csrf_exempt
def Id_Status(request):
        user_id = request.POST.get('user_id')
        print(user_id)
        user_status = User_Status.objects.get(User=user_id)
       
        if request.POST.get('Status') == 'Decline':
                user_status.Status = "Decline_Broadcaster"
                user_status.save()
                return JsonResponse('OK', safe=False) 
        if request.POST.get('Status') == 'Approve':
                user_status.Status = "Broadcaster"
                user_status.save()
        print(user_status.Status)
        return JsonResponse('OK', safe=False) 

@csrf_exempt
def Create_Staff(request):
    if request.method == "POST":
        form =UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user     = authenticate(request, username=username, password=form.cleaned_data.get('password1'))
            login(request, user)

            User_Status.objects.create(User = user,Status= "Staff")
            staff_manager = StaffRoomManager.objects.create(Staff = user)
            staff_manager.add_staff(user)
            
            messages.success(request, f'Account Created for {username}!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            print(form.errors)
            messages.error(request, form.errors)
    else:    
        form =UserRegisterForm()
    return render(request, "accounts/registration.html", {'create_staff': form})



@csrf_exempt
def sendStaffInvitation(request):
        
 
        if request.method == "POST":
                
                form = AddStaffPermission(request.POST)
                if form.is_valid():
                        email = form.cleaned_data['email']
                        permissions = form.cleaned_data['permissions']

                        # set permission for the staff
                        content_type = ContentType.objects.get_for_model(StaffManager)
                        staff = StaffManager.objects.create(email=email)
                        
                        permission_codenames = request.POST.getlist('permissions')
            
                        permissions = Permission.objects.filter(content_type=content_type, codename__in=permission_codenames)
                        staff.user_permissions.set(permissions)
                        staff.save()
                        
                        
                        # send email to staff
                        message = "click the link and fill in the form:\n\nhttp://127.0.0.1:8000/staff/staffRegistration/"
                        send_mail('Staff Invitation!', message, settings.EMAIL_HOST, [email])

                        messages.success(request, f'Invitation Sent!')
                        return JsonResponse('OK', safe=False) 
                
                else:
                        print(form.errors)
                        err = messages.error(request, form.errors)
        else:    
                
                form =AddStaffPermission()
        return render(request, "staff/home.html", {'form': form, "err" : err})

@csrf_exempt
def staffRegistration(request):

        
        if request.method == "POST":
                user_form = UserRegisterForm(request.POST)
                personalinfo_form = AddStaff(request.POST, request.FILES)
                if user_form.is_valid() and personalinfo_form.is_valid():
                        user_form.save()
                        
                        staff = StaffManager.objects.get(email=personalinfo_form.cleaned_data['email'])
                        staff.staff_id = User.objects.get(username=user_form.cleaned_data['username'])
                        staff.fname = personalinfo_form.cleaned_data['fname']
                        staff.lname = personalinfo_form.cleaned_data['lname']
                        staff.birthday = personalinfo_form.cleaned_data['birthday']
                        staff.address = personalinfo_form.cleaned_data['address']
                        staff.id_photo = personalinfo_form.cleaned_data['id_photo']
                        staff.profile_pic = personalinfo_form.cleaned_data['profile_pic']
                        staff.save()
                        
                        print(user_form)
                        print(personalinfo_form)
                        
                        messages.success(request, f'Account Created!')
                        return redirect("staff_home")
                else:
                        print(user_form.errors)
                        print(personalinfo_form.errors)
                        messages.error(request, user_form.errors)
                        messages.error(request, personalinfo_form.errors)
                        
                        user_form = UserRegisterForm()
                        personalinfo_form = AddStaff()
        else:
                user_form = UserRegisterForm()
                personalinfo_form = AddStaff()
                
        return render(request, "staff/include/staff_registration.html", locals())
        

@csrf_exempt
def Add_Dev_Project(request):
        ToDoProject_Dev.objects.create(
                Name    = request.POST.get('Project_Name'),
                Coder   =  User.objects.get(username = request.POST.get('Coder')),
                Staff   = request.user
                )
        return JsonResponse('OK', safe=False) 

@csrf_exempt
def Add_Dev_List(request):
        ToDolist_Dev.objects.create(
                ToDoProject     = ToDoProject_Dev.objects.get(id=int(request.POST.get('project_id'))),
                Title           = request.POST.get('title'),
                Message         = request.POST.get('message'),
                Coder           = User.objects.get(username = request.POST.get('coder')),
                Staff           = request.user
                )
        return JsonResponse('OK', safe=False) 

