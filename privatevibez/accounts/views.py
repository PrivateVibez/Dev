from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import QueryDict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import *
from .models import *
from rooms.views import display_user_availed_item_in_broadcaster_room
from base.views import paginate_list
from django.core.paginator import Paginator
from chat.models import Private, Public
from rooms.models import *
from django.contrib.auth.decorators import login_required
from staff.models import StaffManager, PrivatevibezRevenue
from django.utils import timezone
from cryptography.fernet import Fernet
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import secrets
import datetime
import json
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict
from .serializers import User_DataSerializer, Room_DataSerializer,UserSerializer
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
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
        print(user,flush=True)
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
    
    
    if request.user.is_authenticated:
        user_datas        = User_Data.objects.get(User =  request.user)
        
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
            messages.success(request, f'You have created an account {username}! enjoy vibing!')
            
            return redirect("Main_home")
        
        else:
            print(form.errors,flush=True)
            messages.error(request, form.errors)
    else:    
        form =UserRegisterForm()
    return render(request, "accounts/registration.html", {'registration_form': form})



def RegistrationWithPromotionCode(request):
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
                messages.success(request, f'You have created an account {username}! enjoy vibing!')
                
                return redirect(request.META.get('HTTP_REFERER'))
            
            else:
                messages.error(request, form.errors)
        else:    
            form =UserRegisterForm()
        
        return redirect(request.META.get('HTTP_REFERER'))



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
        
        max_size = 5 * 1024 * 1024
        
        try:
            Id_File = request.FILES['id_File']
            second_id_File = request.FILES['second_id_File']
            # Your code to process the uploaded file
        except MultiValueDictKeyError:
            # Handle the case where 'file' key is not present
            return JsonResponse("please upload your ID", status=500, safe=False) 
        
        
        if Id_File is not None and second_id_File is not None:
            if  request.FILES['id_File'].size > max_size and request.FILES['second_id_File'].size > max_size:
                return JsonResponse(f'please upload a file that is less than 5mb', status=500, safe=False)
            else:
                user_data               = User_Data.objects.get(User = request.user)
                user_data.Id_File       = request.FILES['id_File']
                user_data.Second_Id_File= request.FILES['second_id_File']
                user_status             = User.objects.get(id=request.user.id)
                user_status.Status      = "Pending_Broadcaster"
                
                user_data.save()
                user_status.save()
            
                if not Room_Data.objects.filter(User = request.user).exists():
                    Room_Data.objects.create(User = request.user)
                    
                return JsonResponse('successfully saved', safe=False)

@csrf_exempt
def Buy_Vibez(request):
    
        user_data = User_Data.objects.get(User = request.user)
        vibez = int(request.POST.get('Vibez'))
        
        user_data.Vibez += vibez
        user_data.save()
        
        privatevibez = PrivatevibezRevenue.objects.first()
        
        if privatevibez:
            cash = privatevibez.Vibe_Cost * float(vibez)
            
            if privatevibez.Total_Cash is not None:
                privatevibez.Total_Cash += cash
            else:
                privatevibez.Total_Cash = cash
            
            privatevibez.save()
            total_cash = privatevibez.Total_Cash
            total_slot_vibez = privatevibez.Slot_Machine_Revenue
            
        channel_layer = get_channel_layer()
        channel_name = "privatevibezrevenue"
        print(channel_name,flush=True)
        
        # Prepare data to send
        data = {
            "total_cash": total_cash,
            "total_user_vibez": User_Data.objects.aggregate(Sum('Vibez')),
            "total_slot_vibez": total_slot_vibez,
        }
        
        # Send the data to the WebSocket consumer
        async_to_sync(channel_layer.group_send)(
            channel_name,
            {"type": "show.updatedRevenue", "data": data}
        )
            
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
    
    broadcaster = User_Data.objects.get(User = request.POST.get("room"))
    room_id     = Room_Data.objects.get(User = broadcaster.User)
    user       = User_Data.objects.get(User =  request.POST.get("user"))
    note       = request.POST.get('note')
    vibez      = int(request.POST.get('Vibez')) if request.POST.get('Vibez') else None
    
    if vibez is not None:
        if user.Vibez >= vibez:
            real_vibez = user.Vibez - vibez
            

            broadcaster.Vibez += vibez
            broadcaster.save()
            user.Vibez -= vibez
            user.save()
            
            
            item = Item_Availed.objects.create(Room=room_id,User=user.User,Item="Sent Vibez",Cost=vibez,Note=note)
            
            display_user_availed_item_in_broadcaster_room(user,item,room_id)
            
            return JsonResponse({'data':'sent vibez!'}, safe=False)
        else:
            return JsonResponse(f'not enough vibez',status=500,safe=False)
    else:
        return JsonResponse(f'enter a valid amount',status=500,safe=False)


@csrf_exempt
def Profile_Pic(request):
    
    user_data         = User_Data.objects.get(User = request.user)
    image             = request.FILES['file']
    
    if image:
        max_file_size = 5 * 1024 * 1024  # 5 MB
        if image.size > max_file_size:
            messages.error(request, "Image too large. Size should not exceed 5 MB.")
            return JsonResponse('OK', safe=False) 
        else:
            user_data.Image = image
            user_data.save()
            return JsonResponse('OK', safe=False) 

    
    

@csrf_exempt
def bio_info(request):
    
    user_data               = User_Data.objects.get(User = request.user)
    room_data               = Room_Data.objects.get(User = request.user)
    
    promotion_code          = request.POST.get('promotion_code')
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
    
    print(promotion_code,flush=True)
    if promotion_code is not None and promotion_code != "":
        if Promotion.objects.filter(Promotion_Code = promotion_code).exists():
            promotion = Promotion.objects.get(Promotion_Code = promotion_code)
            
            if promotion.Promotion_Registration_Limit > 0:
                
                promotion.Promotion_Registration_Limit -= 1
                promotion.save()
                room_data.Room_promotion = promotion
                
            else:
                return JsonResponse('Promotion Code Limit Reached', safe=False)
        else:
            return JsonResponse('Invalid Promotion Code', safe=False)
    else:
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
                                                    "image": user_data.Image.url,
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

                print(broadcaster_data,flush=True)
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
    
    
    
def avail_subscription(request):
    
    if request.method == "POST":
        
        subscription = request.POST.get('subscription_type')
        
        if subscription is not None:
            user = request.user
            user_data = User_Data.objects.get(User = user)
            
            subscription = Subscription.objects.get(Name = subscription)
            
            if user_data.Subscription_Type is None:
                user_data.Subscription_Type = subscription
                user_data.Vibez += subscription.Vibez
                user_data.Free_spins += subscription.Slots
                user_data.save()
                return JsonResponse({"data":f'you have successfully subscribed to {user_data.Subscription_Type} plan. Enjoy vibing!'}, safe=False)
            else:
                
                return JsonResponse({"data":f'you are already subscribed to {user_data.Subscription_Type} a plan.'},status=500, safe=False)
            

        
        return JsonResponse(request.POST, safe=False)
    
    
def unsubscribe(request):
    
    if request.method == "POST":
        
        user = request.user
        
        user_data = User_Data.objects.get(User = user)
        subscription = user_data.Subscription_Type
        user_data.Subscription_Type = None
        user_data.save()
        
        return JsonResponse({"data":f'you have successfully unsubscribed from {subscription}'}, safe=False)
    
def countdown_timer(code):
    
    promotion_earning = code.Promotion_Earning
    promotion_registration_limit = code.Promotion_Registration_Limit
    promotion_duration = code.Duration  # This is a datetime.datetime object

    # Calculate the time remaining until the promotion_duration
    now = datetime.datetime.now()
    time_remaining = promotion_duration - now

    # Extract days, hours, minutes, and seconds from the timedelta
    days = time_remaining.days
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60) 
    
    return {
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
    }  
    
def BroadcasterRegistration(request, code):
        
        if code is not None:
                
                code = get_object_or_404(Promotion, Promotion_Code=code)
                data = countdown_timer(code)
                
                if request.method == "POST":
        
                    registration_form =UserRegisterForm(request.POST)
                    if registration_form.is_valid():
                        registration_form.save()
                        
                        username = registration_form.cleaned_data.get('username')
                        user     = authenticate(request, username=username, password=registration_form.cleaned_data.get('password1'))
                        
                        login(request, user)
                        
                        if not User_Data.objects.filter(User = user).exists():
                            User_Data.objects.create(User = user,Vibez = "0")
                            
                        User_Status.objects.create(User = user,Status= "User")
                        messages.success(request, f'You have created an account {username}! enjoy vibing!')
                        
                        return redirect("Main_home")
                    
                    else:
                        messages.error(request, registration_form.errors)
                else:    
                    registration_form =UserRegisterForm()
                return render(request, "accounts/registration_broadcaster.html", locals())
                            
                    