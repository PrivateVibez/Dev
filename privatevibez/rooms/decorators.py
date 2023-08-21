from django.shortcuts import redirect
from rooms.models import Room_Data
from django.contrib.auth import get_user_model
User = get_user_model()


def check_user_blocked_ip(redirect_url='/'):
  def decorator(view_func):
    def check_user(request,*args, **kwargs):
      
      if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        check_user_status(redirect_url='/')
 
        try:
          slug = kwargs.get('Broadcaster')
          if user.Country:
            user_country = user.Country
            user_region = user.Region
          else:
              user_region = None
              user_country = None

          
          
          broadcaster = Room_Data.objects.get(User__username=slug)
          blocked_countries = broadcaster.Blocked_Countries.values_list('Country__code2',flat=True)
          blocked_regions = broadcaster.Blocked_Regions.values_list('Region__display_name',flat=True)
          

          
          if user_region not in blocked_regions and user_country not in blocked_countries:
            
            return view_func(request, *args, **kwargs)
          else:
            return redirect(redirect_url)
        except (User.DoesNotExist, Room_Data.DoesNotExist):
                return redirect(redirect_url)
      else:
        return view_func(request, *args, **kwargs)
      
      
    return check_user
  return decorator


def check_user_status(redirect_url='/'):
  def decorator(view_func):
    def check_user(request,*args, **kwargs):
      
      if request.user.is_authenticated:
          user = User.objects.get(username=request.user)
          broadcaster_username = kwargs.get('Broadcaster')
          user_status = user.Status
          if user_status == "Pending_Broadcaster" and user.username == broadcaster_username:
              print(user_status,flush=True)
              return redirect(redirect_url)
          elif user_status == "Declined_Broadcaster":
              print(user_status,flush=True)
              return redirect(redirect_url)
          
          else:
            return view_func(request, *args, **kwargs)
      else:
        return view_func(request, *args, **kwargs)
            

      
      
    return check_user
  return decorator