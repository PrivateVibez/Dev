from django.db import models
from django.contrib.auth.models import Permission
from django.conf import settings
# Create your models here.

class ToDoProject_Dev(models.Model):
    Name      = models.CharField(max_length=200,null=True,blank=True)
    Coder     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Staff     = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE, related_name = 'ToDoProject_Dev_Staff')
    Timestamp = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.Name)


class ToDolist_Dev(models.Model):
    ToDoProject = models.ForeignKey(ToDoProject_Dev, on_delete=models.CASCADE)
    Title       = models.CharField(max_length=100,null=True,blank=True)
    Message     = models.CharField(max_length=200,null=True,blank=True)
    Coder       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'ToDolist_Dev_Coder')
    Staff       = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE, related_name = 'ToDolist_Dev_Staff')
    Done        = models.BooleanField(default=False)
    Timestamp   = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.ToDoProject)
    
    
class StaffRoomManager(models.Model):
    Staff = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE, related_name = 'Staff_Name')
    staff_list = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True, symmetrical=False, related_name="staff_list")


    def add_staff(self, user):
        self.staff_list.add(user)
        self.save()

    def remove_staff(self, user):
        self.staff_list.remove(user)
        self.save()
        
    def total_staff(self):
        return self.staff_list.count()

    def __str__(self):
        return self.Staff.username
    

class StaffManager(models.Model):
        email = models.CharField(max_length=100,null=True,blank=True, unique=True)
        staff_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
        fname = models.CharField(max_length=100,null=True,blank=True)
        lname = models.CharField(max_length=100,null=True,blank=True)
        birthday = models.DateField(null=True, blank=True)
        address = models.CharField(max_length=100,null=True)
        id_photo = models.ImageField(upload_to='ID',null=True,blank=True)
        profile_pic = models.ImageField(upload_to='profile_pic',null=True,blank=True)
        user_permissions = models.ManyToManyField(Permission, blank=True)
        logout_time = models.DateTimeField(null=True, blank=True)
        class Meta:
            permissions = [
                ("can_add_staff", "Can add staff"),
                ("can_edit_staff", "Can edit a staff"),
                ("can_delete_staff", "Can delete a staff"),
                ("can_view_staff", "Can view a staff"),
                ("can_view_dashboard", "Can view a dashboard"),
                ("can_view_id_check", "Can view a ID Check"),
                ("can_view_bad_acters", "Can view a bad acters"),
                ("can_view_todo_list", "Can view a todo list"),
                ("can_view_inbox", "Can view a inbox"),
            ]
        
        def add_staff(self, user):
            self.staff_id.add(user)
            self.save()

        def remove_staff(self, user):
            self.staff_id.remove(user)
            self.save()
            
        def __str__(self):
            return self.email
