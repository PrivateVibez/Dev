from django.shortcuts import render
from accounts.models import *
from rooms.models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib import messages
from staff.models import StaffManager
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()




def home(request):

                
        if request.user.is_authenticated :
                blocked_broadcasters = Bad_Acters.objects.filter(Reporty = request.user.id)
                try:
                        
                        user_status_data = User_Status.objects.get(User = request.user)
                        user_status      = user_status_data.Status
                        
                
                        user_status      = user_status_data.Status
                        
                        rooms = Room_Data.objects.all()
                        rooms_list = []
                        blocked_user_ids = [b.Reported.id for b in blocked_broadcasters]
                        
                        for room in rooms:
                                if room.User.id in blocked_user_ids:
                                        pass
                                else:
                                                rooms_list.append({'User': room.User,
                                                'Tab': room.Tab,
                                                'Goal': room.Goal,
                                                'Public_Chat': room.Public_Chat,
                                                'Private_Chat': room.Private_Chat,
                                                'Private_Chat_Price': room.Private_Chat_Price,
                                                'Price_MMM_button': room.Price_MMM_button,
                                                'Price_OH_button': room.Price_OH_button,
                                                'Price_OHYes_button': room.Price_OHYes_button,
                                                'Duration_MMM_button': room.Duration_MMM_button,
                                                'Duration_OH_button': room.Duration_OH_button,
                                                'Duration_OHYes_button': room.Duration_OHYes_button,
                                                'Strength_MMM_button': room.Strength_MMM_button,
                                                'Strength_OH_button': room.Strength_OH_button,
                                                'Strength_OHYes_button': room.Strength_OHYes_button,
                                                
                                                })
                                        
                        if user_status == 'Staff':
                                room_users_data = User_Data.objects.all()
                           
                        else:
                                user_data        = User_Data.objects.get(User = request.user)
                                pass
                        
                except(User_Status.DoesNotExist, User_Data.DoesNotExist):
                        if StaffManager.objects.filter(staff_id_id = request.user).exists():
                                return redirect('staff/')
        else:
                room_users_data = User_Data.objects.all()
                
        
        rooms_list = Room_Data.objects.all()

        room_users_data = User_Data.objects.all()

                


        return render(request, "base/home.html", locals())




