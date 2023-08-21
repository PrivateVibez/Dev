from django.shortcuts import render
from django.contrib.auth.models import User, Group, Permission
from accounts.models import *
from rooms.models import *
from .models import *
import os
from django.conf import settings
from chat.models import Staff
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
from .forms import UserRegisterForm, UpdateStaffInfoForm
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse as httpresponse
from django.forms.models import model_to_dict
from django.core import serializers
from rest_framework.renderers import JSONRenderer
import datetime
from django.db.models.fields.files import ImageFieldFile
import json
from django.shortcuts import get_object_or_404
from django.views import View
from .serializers import StaffMessagesSerializer, UserStatusSerializer, StaffSerializer
from staff.models import Memos
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.

def home(request):
        
        print(request.user,flush=True)
        if request.user.is_authenticated and StaffManager.objects.filter(staff_id=request.user).exists():
                bad_acters_list = []
                
                pending = User.objects.filter(Status='Pending_Broadcaster')
                pending_user_id = list(pending.values_list('id',flat=True))

                decline_messages = Decline_Message.objects.all()
                
                user_data = User_Data.objects.filter(User__id__in=pending_user_id)
                
                users_status = User_Status.objects.all()
                users_data = User_Data.objects.all()
                
                bad_acters = Bad_Acters.objects.all()
                total_bad_acters_count = bad_acters.count()
                
                for bad_acter in bad_acters:
                        bad_acters_list.append({
                                                
                                                'reporty': None if bad_acter.Reporty is None else bad_acter.Reporty,
                                                'reported': None if bad_acter.Reported is None else bad_acter.Reported,
                                                'message': None if bad_acter.Message is None else bad_acter.Message,
                                                'status': None if User_Status.objects.get(User=bad_acter.Reporty) is None else User_Status.objects.get(User=bad_acter.Reporty).Status,
                                                'total_reports': Bad_Acters.objects.filter(Reporty = bad_acter.Reporty).count(),})
                
                to_do_projects_dev = ToDoProject_Dev.objects.all()
                to_do_lists_Dev = ToDolist_Dev.objects.all()
                to_do_lists_Dev_count = to_do_lists_Dev.count
                
                # staff chat
                try:
                        broc_manager = StaffRoomManager.objects.get(Staff=request.user)
                        room_name    = User.objects.get(username=request.user.username)
                        print(room_name)
                        broc_staff_list = StaffRoomManager.objects.all()
                except StaffRoomManager.DoesNotExist:
                        broc_manager = None
                        room_name    = None
                        broc_staff_list = None
                
                sessions_info = []
                staff_ids = []
                
                active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

                # Filter sessions based on the is_staff field of the related User model
                staff_sessions = [s for s in active_sessions if s.get_decoded() and User.objects.filter(pk=s.get_decoded().get('_auth_user_id'), is_staff=True).exists()]

                staff_list = StaffManager.objects.all()
                
                # Query all existing Staff
                for staff in staff_list:

                        try:
                                
                                current_staff = User.objects.get(email=staff.email)
                                login_time = current_staff.last_login
                        
                        except User.DoesNotExist:
                                login_time = None
                                
                        if staff.staff_id_id is not None:   
                                sessions_info.append({
                                'user_id': None if staff.staff_id_id is None else staff.staff_id_id,
                                'username': staff.fname if staff.fname else None,
                                'login_time': login_time,
                                'logout_time': None if staff.logout_time is None else staff.logout_time.strftime("%Y-%m-%d %H:%M:%S"),    
                                'is_session_active': False if current_staff else 'Pending',
                                
                                })
                        
                        for session in staff_sessions:
        
                                session_data = session.get_decoded()
                                user_id = session_data.get('_auth_user_id')
                                
                                try:
                                        
                                        user = User.objects.get(pk=user_id)
                                except User.DoesNotExist:
                                        user = None
                                
                                if user is not None and StaffManager.objects.filter(staff_id=user).exists():
                                        if staff.staff_id_id == user.id:
                                                for session_info in sessions_info:
                                                        if session_info['user_id'] == user.id:
                                                                session_info['login_time'] = user.last_login
                                                                session_info['logout_time'] = staff.logout_time
                                                                session_info['is_session_active'] = True
                                                                break

                                                
                        

                return render(request, "staff/home.html", locals())
        
        else:
                messages.info(request,"Please login")
                return redirect("login")
        
@csrf_exempt
def Id_Status(request):
        user_id = request.POST.get('User_id')
     
        user_status = User.objects.get(id=user_id)
       
        if request.POST.get('Status') == 'Decline':
                
                user_status.Status = "Decline_Broadcaster"
                user_status.Decline_Message = request.POST.get('message')
                user_status.save()
                
                user_data = User_Data.objects.filter(User__Status="Pending_Broadcaster")
                serializer = UserStatusSerializer(user_data, many=True)
                
                return JsonResponse({'data':serializer.data}, safe=False) 



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
def deleteStaff(request):
        
   
        staff_id = request.GET.get('staff_id')
       
        staff = User.objects.get(id=staff_id)
        staff.delete()
        
        return JsonResponse({'message': 'Staff deleted successfully.'})


@csrf_exempt
def getPermission(request):
        
        staff = request.GET.get('staff')
        staff = User.objects.get(id=staff)
        staff_permission = staff.user_permissions.values('name','codename')
        print(staff_permission,flush=True)
 
        return JsonResponse ({'data' : list(staff_permission)}) 

def encode_datetime(obj):
    """
    Extended encoder function that helps to serialize dates and images
    """
    if isinstance(obj, datetime.date):
        try:
            return obj.strftime('%Y-%m-%d')
        except (ValueError, e):
            return ''

    if isinstance(obj, ImageFieldFile):
        try:
            return obj.path
        except (ValueError, e):
            return ''

    raise TypeError(repr(obj) + " is not JSON serializable")

def getStaffInformation(request):
        
        staff_id = request.GET.get('staff')
        staff = StaffManager.objects.get(staff_id_id=staff_id)
        
        staff_serializer = StaffSerializer(staff)
        
        return JsonResponse ({'data' : staff_serializer.data}) 

@csrf_exempt
def editStaffPermission(request):
        
        if request.method == "POST":

                user = User.objects.get(id=request.POST.get('staff')) 
                permission_codenames = request.POST.getlist('existing_permissions')
                content_type = ContentType.objects.get_for_model(StaffManager)
            
                permissions = Permission.objects.filter(content_type=content_type, codename__in=permission_codenames)
                
                user.user_permissions.set(permissions)
                user.save()
                
                messages.success(request,"Staff permission successfully updated!")
                print(user.user_permissions.all(),flush=True)
        
        
                return JsonResponse('Updated!', safe=False) 

@csrf_exempt
def sendStaffInvitation(request):
        
 
        if request.method == "POST":
                
                form = AddStaffPermission(request.POST)
                if form.is_valid():
                        
                        email = form.cleaned_data['email']
                        permissions = form.cleaned_data['permissions']

                        # set permission for the staff
                        content_type = ContentType.objects.get_for_model(StaffManager)
                        staff, _ = StaffManager.objects.get_or_create(email=email)
                        
                        permission_codenames = request.POST.getlist('permissions')
            
                        permissions = Permission.objects.filter(content_type=content_type, codename__in=permission_codenames)
                        staff.user_permissions.set(permissions)
                        staff.save()
                        
                        
                        # send email to staff
                        message = "click the link and fill in the form:\n\nhttp://127.0.0.1:8000/staff/staffRegistration/"
                        
                        send_mail('Staff Invitation!', message, settings.EMAIL_HOST, [email])

                        messages.success(request, f'Invitation Sent!')
                        return redirect(request.META.get('HTTP_REFERER')) 
                
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
                        
                        
                        # CHECK IF THE EMAIL IS PRESENT IN THE DATABASE
                        try:
                                max_file_size = 5 * 1024 * 1024

                                if personalinfo_form.cleaned_data['id_photo'] and personalinfo_form.cleaned_data['profile_pic']:
                                        id_photo_size = personalinfo_form.cleaned_data['id_photo'].size
                                        profile_pic_size = personalinfo_form.cleaned_data['profile_pic'].size

                                        if id_photo_size > max_file_size or profile_pic_size > max_file_size:
                                                messages.error(request, "The file is too big. File size should not exceed 5MB.")
                                                return redirect(request.META.get('HTTP_REFERER'))

                                
                                staff = StaffManager.objects.get(email=user_form.cleaned_data['email'])
                                
                                if User.objects.filter(email=user_form.cleaned_data['email']).exists():
                                        
                                        pass
                                else:
                                        user_form.save()
                                        
                                user = User.objects.get(username=user_form.cleaned_data['username'])
                                
                                staff_permissions = staff.user_permissions.all()
                                user.user_permissions.set(staff_permissions)
                                
                                staff_chat = StaffRoomManager.objects.create(Staff = user)
                                staff_chat.add_staff(user)
                                
                                staff.staff_id = User.objects.get(username=user_form.cleaned_data['username'])
                                staff.fname = personalinfo_form.cleaned_data['fname']
                                staff.lname = personalinfo_form.cleaned_data['lname']
                                staff.birthday = personalinfo_form.cleaned_data['birthday']
                                staff.address = personalinfo_form.cleaned_data['address']
                                staff.id_photo = personalinfo_form.cleaned_data['id_photo']
                                staff.profile_pic = personalinfo_form.cleaned_data['profile_pic']
                                
                                staff.save()
                                messages.success(request, f'Account Created!')
                                return redirect("staff_home")
                        
                        except StaffManager.DoesNotExist:
                                messages.error(request, "Use the email you were invited with")
                                return redirect(request.META.get('HTTP_REFERER'))
                        

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



@csrf_exempt
def getstaffmessages(request):
        
        if request.method == 'GET':
                staff_id = request.GET.get('staff_id')
                
                user_id = User.objects.get(username = staff_id)
                staff_messages = Staff.objects.filter(Q(From=user_id.id) | Q(From=request.user.id)).order_by('Timestamp')

                serializer = StaffMessagesSerializer(staff_messages, many=True) 
                return JsonResponse({'data': serializer.data}, safe=False)
        
        
def save_memo(request):
        
        if request.method == 'POST':
                
                staff = User.objects.get(id=request.POST.get('staff'))
                subject = request.POST.get('subject')
   
                

                
                memoContent = request.POST.get('memoContent', '')
                
                if memoContent:
                        memo = Memos.objects.create(
                        From = staff,
                        Subject = subject,
                        )
                        
                        recipients = User.objects.filter(Status=request.POST.get('recipient'))
                        
                        project_directory = os.path.dirname(os.path.dirname(__file__))
                        static_folder = os.path.join(project_directory, 'static/memos')
                        
                        file_path = os.path.join(static_folder, str(subject) + '.txt')

                        # Write the memoContent to the file
                        with open(file_path, 'w') as file:
                                file.write(memoContent)
                                
                        for recipient in recipients:
                                memo.To.add(recipient)
                                
                        # Assuming your static folder is located at "static/"
                        # Get the directory where views.py is located
                        views_directory = os.path.dirname(os.path.abspath(__file__))

                        # Create the 'memos' folder inside the views.py directory if it doesn't exist
                        memos_folder = os.path.join(views_directory, 'memos')
                        if not os.path.exists(memos_folder):
                                os.makedirs(memos_folder)

                        # Assuming 'subject' and 'memoContent' are valid variables
                        file_name = str(subject) + '.txt'
                        file_path = os.path.join(memos_folder, file_name)

                        # Write the memoContent to the file
                        with open(file_path, 'w') as file:
                                file.write(memoContent)

                        return HttpResponse('Memo content saved successfully.')
                else:
                        return HttpResponse('No memo content received.')
                        
                        
                        
def getPendingBroadcasters(request):
    
        pending = User.objects.filter(Status='Pending_Broadcaster')
        pending_user_id = list(pending.values_list('id',flat=True))


        user_data = User_Data.objects.filter(User__id__in=pending_user_id)
        
        serializer = UserStatusSerializer(user_data, many=True)
        

        
        return JsonResponse({'data':serializer.data}, safe=False)


def addDeclineMsg(request):
        
        if request.method == "POST":
                message = request.POST.get('decline_message_text')
                Decline_Message.objects.create(Writer=request.user, Message=message)
                messages.success(request, f'Decline Message Added!')
        else:
                pass
        return redirect('staff_home')


def approveBroadcaster(request):
        
        if request.method == "POST":
                
                user_id = request.POST.get('user_id')
                user = User.objects.get(id=user_id)
                user.Status = "Broadcaster"
                user.save()
                
                user_data = User_Data.objects.filter(User__Status="Pending_Broadcaster")
                serializer = UserStatusSerializer(user_data,many=True)
                
                return JsonResponse({'data':serializer.data},safe=False)
        
        
        
def updateStaffData(request):
        
        if request.method == "POST":
                
                user = get_object_or_404(User, id=request.POST.get('staff_id'))
                
                staff = get_object_or_404(StaffManager, staff_id=user.id)
                print(staff,flush=True)
                form = UpdateStaffInfoForm(request.POST, instance=staff)
                
                if form.is_valid():
                        
                        form.save()
                        print(form,flush=True)
                        messages.success(request, f'Staff info successfully updated!')
                        return redirect(request.META.get('HTTP_REFERER'))
                
                else:
                        messages.error(request,form.errors)
                        
                        return redirect(request.META.get('HTTP_REFERER'))