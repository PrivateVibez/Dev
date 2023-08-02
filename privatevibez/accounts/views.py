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
            messages.error(request, f'something went wrong!')
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
        
        




