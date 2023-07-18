from django.shortcuts import render
from django.contrib.auth.models import User
from accounts.models import *
from rooms.models import *
from staff.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages



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
        try:
            broc_manager = StaffRoomManager.objects.get(Staff=request.user)
            broc_staff_list = broc_manager.staff_list.all()
        except StaffRoomManager.DoesNotExist:
            broc_staff_list = []
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

