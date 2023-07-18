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
