from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import *
from .models import *
from base.views import paginate_list
from django.core.paginator import Paginator
from chat.models import Private, Public
from rooms.models import *
from django.contrib.auth.decorators import login_required
from staff.models import StaffManager
from django.utils import timezone
from cryptography.fernet import Fernet
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import secrets
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict
from .serializers import User_DataSerializer, Room_DataSerializer,UserSerializer
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
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
            
        messages.success(request, f'Thanks for coming back {username}!')
           
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
        user_status.Status      = "Pending_Broadcaster"
        
        user_data.save()
        user_status.save()
        
        if not Room_Data.objects.filter(User = request.user).exists():
            Room_Data.objects.create(User = request.user)
            
        return JsonResponse('OK', safe=False) 

@csrf_exempt
def Buy_Vibez(request):
    
        user_data = User_Data.objects.get(User = request.user)
        vibez = int(request.POST.get('Vibez'))
        user_data.Vibez += vibez
        user_data.save()
        messages.success(request, f'You have successfully bought {vibez} vibez!')
        
        return JsonResponse({'data':vibez}, safe=False) 

@csrf_exempt
def Bad_Acters_Add(request):
        
    try:
        reporty_username = request.POST.get('reporty')
        reported_username = request.POST.get('reported')
        message = request.POST.get('message')

        reporty_user = User.objects.get(username=reporty_username)
        reported_user = User.objects.get(username=reported_username)

        try:
            bad_actor = Bad_Acters.objects.get(Reporty=reporty_user, Reported=reported_user)
            # Handle the case where the object already exists
            messages.error(request,"Broadcaster Already Reported!")
            print("already reported",flush=True)
        except ObjectDoesNotExist:
            # Object does not exist, create it
            bad_actor = Bad_Acters.objects.create(Reporty=reporty_user, Reported=reported_user, Message=message)
            messages.success(request,"Broadcaster Reported!")
    except Exception as e:
        # Handle the exception that occurred during creation
        print(e,flush=True)
        
    return JsonResponse({'data':f'You have successfully reported {reported_username}'}, safe=False) 

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
        
        message = f"You have successfully sent {vibez} vibez to {broacaster.User.username}"
    else:
        messages.error(request, "not enough vibez!")

    return JsonResponse({'data':message}, safe=False)

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
    
    
            # Get the channel layer
    channel_layer = get_channel_layer()
    channel_name = "staff"
    
    # Prepare data to send
    data = {
            "user": user_data,
    }
    
    # Send the data to the WebSocket consumer
    async_to_sync(channel_layer.group_send)(
            channel_name,
            {"type": "showPending.Broadcaster", "data": data}
    )
    
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


def filter_broadcasters(user,user_country,user_region,broadcaster_gender):

    
    if broadcaster_gender is not None and broadcaster_gender != "FEATURED":
            broadcasters = Room_Data.objects.filter(Tab=broadcaster_gender,User__Status="Broadcaster")
    else:
            broadcasters = Room_Data.objects.filter(User__Status="Broadcaster")
 
    
    user_ids = broadcasters.values_list('User__id', flat=True)
    users = User.objects.filter(id__in=user_ids)    
                                                
    combined_fields_list = []
    for user in users:
            user_data_list = User_Data.objects.filter(User=user)
            room_data_list = Room_Data.objects.filter(User=user)
            
            for user_data in user_data_list:
                    
                    combined_fields_list.append({
                                                    "user_id": user.id,
                                                    "username": user.username,
                                                    "Image": user_data.Image.url,
                                                    })

    
    rooms_list = []
    
    for broadcaster in broadcasters:
                                            
            country_blocked = False
            region_blocked = False
            for blocked_country in broadcaster.Blocked_Countries.all():
                    if blocked_country.Country.code2 == user_country:
                            country_blocked = True
                            break  # If the user's country is blocked, no need to check other blocked countries
            
            for blocked_region in broadcaster.Blocked_Regions.all():
                    if blocked_region.Region.display_name == user_region:
                            region_blocked = True
                            break
                        
            if country_blocked or region_blocked:
                    rooms_list.append(broadcaster.User.id)
                    
    
            for room in rooms_list:
    
                    if any(item["user_id"] == room for item in combined_fields_list):
                            combined_fields_list = [item for item in combined_fields_list if item["user_id"] != room]
                            
                            
            if Bad_Acters.objects.filter(Reporty = user).exists():
                
                    blocked_broadcasters = Bad_Acters.objects.filter(Reporty = request.user.id)
                    
                    for blocked_broadcaster in blocked_broadcasters:
                        
                            if any(item == blocked_broadcaster.Reported.id for item in combined_fields_list):
                                    combined_fields_list = [item for item in room_list if item != blocked_broadcaster.Reported.id]
    
    return combined_fields_list



def get_broadcaster(request):
        
        if request.method == 'GET':
            items_per_page = 4  # Number of items per page
            page_number = request.GET.get('page', 1) 
            broadcaster_gender = request.GET.get('Tab')
            
            if request.user.is_authenticated:
                
                user = request.user
                user_country = user.Country
                user_region = user.Region
                
                broadcaster_data = filter_broadcasters(user,user_country,user_region,broadcaster_gender) 
                broadcaster_data = paginate_list(page_number, broadcaster_data, items_per_page)

                return render(request, "base/home.html", locals())          
 
            else:
                if request.user.is_anonymous:
                    
                        user = request.user
                        guest_ip = request.session.get('ip_address')
                        guest_country = request.session.get('guest_country')
                        guest_region = request.session.get('guest_region')
                        
                        broadcaster_data = filter_broadcasters(user,guest_country,guest_region,broadcaster_gender)
                        broadcaster_data = paginate_list(page_number, broadcaster_data, items_per_page)

                        print(broadcaster_data,flush=True) 
                        return render(request, "base/home.html", locals()) 



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