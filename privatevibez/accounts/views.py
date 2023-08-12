from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import *
from .models import *
from chat.models import Private, Public
from rooms.models import *
from django.contrib.auth.decorators import login_required
from staff.models import StaffManager
from django.utils import timezone
from cryptography.fernet import Fernet
import secrets
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict
from .serializers import User_DataSerializer, Room_DataSerializer,UserSerializer
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

def Logout(request):
    
    # DELETE BOTH PRIVATE AND PUBLIC CHATS ONCE SESSION IS TERMINATED
    
    # Private.objects.filter(From_id = request.user).delete()
    # Public.objects.filter(User_id = request.user).delete()
    
    if StaffManager.objects.filter(staff_id = request.user).exists():
        StaffManager.objects.filter(staff_id = request.user).update(logout_time = timezone.now())
    logout(request)
    messages.error(request, 'You are logged out')
    return redirect('Main_home')
 
def Login(request):
    
    if request.POST:
        username = request.POST.get('username')
        password =request.POST.get('password')

        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Thanks for coming back {username}!')
            
            if user.is_staff == False:
                try:
                    status = User_Status.objects.get(User = request.user).Status
                    if status:
                        status = User_Status.objects.get(User = request.user).Status

                        if status == "Broadcaster":
                                return redirect(f'/room/{username}')
                        else:
                            if StaffManager.objects.filter(staff_id = request.user).exists():
                                return redirect('staff_home')
                except Exception as e:
                    return redirect('login')
            else:
                return redirect('staff_home')
                        
        else:
            
            messages.error(request, f"wrong password or username. Please try again, If you don't have an account, please create one.")
        return redirect('Main_home') 
    return render(request,'accounts/login.html')

    



def Registration(request):
    if request.method == "POST":
        form =UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user     = authenticate(request, username=username, password=form.cleaned_data.get('password1'))
            login(request, user)
            if not User_Data.objects.filter(User = user).exists():
                User_Data.objects.create(User = user,Vibez = "0")
            User_Status.objects.create(User = user,Status= "User")
            messages.success(request, f'Account Created for {username}!')
            return redirect("Main_home")
        else:
            messages.error(request, form.errors)
    else:    
        form =UserRegisterForm()
    return render(request, "accounts/registration.html", {'registration_form': form})



@login_required(login_url='login')
def Registration_Broadcaster(request):
    menu_items = Menu_Data.objects.filter(User=request.user)
    dice_data = Dice_Data.objects.filter(User=request.user)
    if User_Data.objects.filter(User = request.user).exists():
        user_data   = User_Data.objects.get(User = request.user)
        context = {'user_datas':user_data}

    return render(request, "accounts/registration_broadcaster.html", locals())
    
@csrf_exempt
def Registration_Broadcaster_info(request):
        user_data            = User_Data.objects.get(User = request.user)
        user                 = request.user
        user.first_name      = request.POST.get('first_name')
        user.last_name       = request.POST.get('last_name')
        user_data.Birth_Date = request.POST.get('Birth_date')

        user.save()
        user_data.save()
        return JsonResponse('OK', safe=False) 

@csrf_exempt
def Registration_Broadcaster_ID(request):
        user_data               = User_Data.objects.get(User = request.user)
        user_data.Id_File       = request.FILES['file']
        user_status             = User.objects.get(id=request.user.id)
        user_status.Status = "Pending_Broadcaster"
        user_data.save()
        user_status.save()
        if not Room_Data.objects.filter(User = request.user).exists():
            Room_Data.objects.create(User = request.user)
        return JsonResponse('OK', safe=False) 

@csrf_exempt
def Buy_Vibez(request):
        user_data = User_Data.objects.get(User = request.user)
        user_data.Vibez += int(request.POST.get('Vibez'))
        user_data.save()
        return JsonResponse('OK', safe=False) 

@csrf_exempt
def Bad_Acters_Add(request):
    Bad_Acters.objects.create(
        Reporty  = User.objects.get(username = request.POST.get('reporty')),
        Reported = User.objects.get(username = request.POST.get('reported')),
        Message  = request.POST.get('message')
    )
    return JsonResponse('OK', safe=False) 
@csrf_exempt
def Send_Vibez(request):
    broacaster = User_Data.objects.get(User = request.POST.get("room"))
    user       = User_Data.objects.get(User =  request.POST.get("user"))
    vibez      = int(request.POST.get('Vibez'))
    real_vibez = user.Vibez - vibez
    if real_vibez >= 0:
        broacaster.Vibez += vibez
        broacaster.save()
        user.Vibez -= vibez
        user.save()

    return JsonResponse('OK', safe=False)

@csrf_exempt
def Profile_Pic(request):
    user_data         = User_Data.objects.get(User = request.user)
    user_data.Image   = request.FILES['file']
    user_data.save()
    return JsonResponse('OK', safe=False) 
@csrf_exempt
def bio_info(request):
    user_data               = User_Data.objects.get(User = request.user)
    room_data               = Room_Data.objects.get(User = request.user)
    print(request.POST)
    user_data.Real_Name     = request.POST.get('Real_Name')
    user_data.Age           = request.POST.get('Age')
    user_data.I_Am          = request.POST.get('I_Am')
    user_data.Interested_In = request.POST.get('Interested_In')
    user_data.Location      = request.POST.get('Location')
    user_data.Language      = request.POST.get('Language')
    user_data.Body_Type     = request.POST.get('Body_Type')
    user_data.Image        = request.FILES['cropped_image']
    
    fernet               = Fernet(settings.FERNET_KEY)
    random_token         = secrets.token_urlsafe(32)
    U_token              = fernet.encrypt(random_token.encode())
    
    user_data.U_token      = U_token
    
    room_data.Tab           = request.POST.get('Tab')
    room_data.save()
    user_data.save()
    return JsonResponse('OK', safe=False) 


def getTotalReports(request):
    
    
    if request.method == "GET":
        
        reporty = request.GET.get('reporty')
        user = Bad_Acters.objects.filter(Reporty = reporty).count()
        return JsonResponse({'data':user}, safe=False)
    
    
def get_IP_Address(request):
    
    if request.method == "POST":
        
        ip_address = request.POST.get('ip_address')
        
        
    
    return JsonResponse({'data':get_client_ip(request)}, safe=False)
        
        

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session's auth hash
            return redirect('password_change_done')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def room_data_func(request,broadcaster_gender,user_country,user_region):
    
    if broadcaster_gender != "FEATURED":
        room_data = Room_Data.objects.filter(User__Status="Broadcaster",Tab=broadcaster_gender)
        room_list = []
        for room in room_data:
            
            country_blocked = False
            region_blocked = False
            for blocked_country in room.Blocked_Countries.all():
                if blocked_country.Country.code2 == user_country:
                    country_blocked = True
                    break  # If the user's country is blocked, no need to check other blocked countries
            
            for blocked_region in room.Blocked_Regions.all():
                if blocked_region.Region.display_name == user_region:
                    region_blocked = True
                    break
            if not country_blocked and not region_blocked:
                room_list.append(room.User.id)
                
                
            if request.user.is_authenticated:
                if Bad_Acters.objects.filter(Reporty = request.user.id).exists():
                        blocked_broadcasters = Bad_Acters.objects.filter(Reporty = request.user.id)
                        for blocked_broadcaster in blocked_broadcasters:
                                if any(item == blocked_broadcaster.Reported.id for item in room_list):
                                        room_list = [item for item in room_list if item != blocked_broadcaster.Reported.id]  
            print(room_list,flush=True)
    else:
        room_data = Room_Data.objects.filter(User__Status="Broadcaster")
        room_list = []
        for room in room_data:
            
            country_blocked = False
            region_blocked = False
            for blocked_country in room.Blocked_Countries.all():
                if blocked_country.Country.code2 == user_country:
                    country_blocked = True
                    break  # If the user's country is blocked, no need to check other blocked countries
            
            for blocked_region in room.Blocked_Regions.all():
                if blocked_region.Region.display_name == user_region:
                    region_blocked = True
                    break
            if not country_blocked and not region_blocked:
                room_list.append(room.User.id)
                
        if request.user.is_authenticated:
            if Bad_Acters.objects.filter(Reporty = request.user.id).exists():
                    blocked_broadcasters = Bad_Acters.objects.filter(Reporty = request.user.id)
                    for blocked_broadcaster in blocked_broadcasters:
                            if any(item == blocked_broadcaster.Reported.id for item in room_list):
                                    room_list = [item for item in room_list if item != blocked_broadcaster.Reported.id]  
        print(room_list,flush=True)

    
    # Retrieve User_Data objects based on the User objects associated with the retrieved Room_Data
    user_data = User_Data.objects.filter(User__in=room_list)
    user_instances = User.objects.filter(user_data__in=user_data)
    
    if broadcaster_gender != "FEATURED":
        room_data = Room_Data.objects.filter(Tab=broadcaster_gender,User__in=user_instances)
    else:
        room_data = Room_Data.objects.filter(User__in=user_instances)  
    
    
    room_data_serializer = Room_DataSerializer(room_data, many=True)
    user_data_serializer = User_DataSerializer(user_data, many=True)
    user_serializer = UserSerializer(user_instances, many=True)
    
    serialized_user_data = JSONRenderer().render(user_data_serializer.data)
    serialized_room_data = JSONRenderer().render(room_data_serializer.data)
    serialized_user_instance = JSONRenderer().render(user_serializer.data)
    
    # If needed, you can decode the JSON bytes to a string
    serialized_user_data_str = serialized_user_data.decode('utf-8')
    serialized_room_data_str = serialized_room_data.decode('utf-8')
    serialized_user_instance_str = serialized_user_data.decode('utf-8')
    # Now you can include the serialized data in your AJAX response
    
    
    response_data = {
        'user_data': serialized_user_data_str,
        'room_data': serialized_room_data_str,
        'user_instance_data':serialized_user_instance_str
        # Other response data if needed
    }

    return response_data

def get_broadcaster(request):
        
        if request.method == 'GET':
            
            broadcaster_gender = request.GET.get('broadcaster')
            if request.user.is_authenticated:
                user = request.user
                user_country = user.Country
                user_region = user.Region
                if broadcaster_gender is not None and broadcaster_gender != "FEATURED":

                    response_data = room_data_func(request,broadcaster_gender,user_country,user_region)
                    
                    return JsonResponse(response_data, safe=False)
                else:
                    response_data = room_data_func(request,broadcaster_gender,user_country,user_region)
                    return JsonResponse(response_data, safe=False)
            else:
                if request.user.is_anonymous:
                        guest_ip = request.session.get('ip_address')
                        guest_country = request.session.get('guest_country')
                        guest_region = request.session.get('guest_region')
                        
                        response_data = room_data_func(request,broadcaster_gender,guest_country,guest_region)
                        return JsonResponse(response_data, safe=False)



def changepassword(request):

    if request.method == "POST":
        
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            
            pass1 = form.cleaned_data['password1']
            pass2 = form.cleaned_data['password2']
            
            if pass1 == pass2:
                user = request.user
                user.set_password(pass1)
                user.save()
                update_session_auth_hash(request, user)

                messages.success(request,"Password Changed!")
                return redirect(request.META.get('HTTP_REFERER'))
            
        else:
            messages.error(request,"Password Not match!")
            print(form.errors,flush=True)
            
            
def change_email(request):
    
    
    if request.method == "POST":
        
        form = ChangeEmailForm(request.POST)
        
        if form.is_valid():
            
            email = form.cleaned_data['email']
            user = request.user
            user.email = email
            user.save()
            messages.success(request,"Email successfully changed!")
        else:
            messages.error(request,"Something went wrong")
            
        return redirect(request.META.get('HTTP_REFERER'))