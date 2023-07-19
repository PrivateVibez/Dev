from django.db import models

# Create your models here.

class ToDoProject_Dev(models.Model):
    Name      = models.CharField(max_length=200,null=True,blank=True)
    Coder     = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    Staff     = models.ForeignKey('auth.User',null=True, on_delete=models.CASCADE, related_name = 'ToDoProject_Dev_Staff')
    Timestamp = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.Name)


class ToDolist_Dev(models.Model):
    ToDoProject = models.ForeignKey(ToDoProject_Dev, on_delete=models.CASCADE)
    Title       = models.CharField(max_length=100,null=True,blank=True)
    Message     = models.CharField(max_length=200,null=True,blank=True)
    Coder       = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name = 'ToDolist_Dev_Coder')
    Staff       = models.ForeignKey('auth.User',null=True, on_delete=models.CASCADE, related_name = 'ToDolist_Dev_Staff')
    Done        = models.BooleanField(default=False)
    Timestamp   = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.ToDoProject)
    
    
class StaffRoomManager(models.Model):
    Staff = models.ForeignKey('auth.User',null=True, on_delete=models.CASCADE, related_name = 'Staff_Name')
    staff_list = models.ManyToManyField('auth.User', null=True, blank=True, symmetrical=False, related_name="staff_list")


    def add_staff(self, user):
        self.staff_list.add(user)
        self.save()

    def remove_fan(self, user):
        self.staff_list.remove(user)
        self.save()
        
    def total_staff(self):
        return self.staff_list.count()

    def __str__(self):
        return self.Staff.username
