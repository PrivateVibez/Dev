from django.shortcuts import render
from accounts.models import *
from rooms.models import *
from django.contrib.auth.models import User



def home(request):
        if request.user.is_authenticated :
                user_status_data = User_Status.objects.get(User = request.user)
                user_status      = user_status_data.Status
                print(type("Staff"))
                if user_status == 'Staff':
                        room_users_data = User_Data.objects.all()
                        print(user_status)
                else:
                        user_data        = User_Data.objects.get(User = request.user)
                        pass
        else:
                room_users_data = User_Data.objects.all()
        rooms = Room_Data.objects.all()

                


        return render(request, "base/home.html", locals())




