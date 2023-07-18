from django.db import models
class User_Status(models.Model):
    User       = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    Status     = models.CharField(max_length=20)
    Timestamp  = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.User)


class User_Data(models.Model):
    User           = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    Birth_Date     = models.CharField(null=True,blank=True, max_length=500)
    Real_Name      = models.CharField(max_length=200,null=True,blank=True)
    Age            = models.IntegerField(null=True,blank=True)
    I_Am           = models.CharField(max_length=200,null=True,blank=True)
    Interested_In  = models.CharField(max_length=200,null=True,blank=True)
    Location       = models.CharField(max_length=200,null=True,blank=True)
    Language       = models.CharField(max_length=200,null=True,blank=True)
    Body_Type      = models.CharField(max_length=200,null=True,blank=True)
    Vibez          = models.IntegerField(null=True,blank=True,default=0)
    Image          = models.ImageField(upload_to='profile_pic',null=True,blank=True)
    Id_File        = models.ImageField(upload_to='ID',null=True,blank=True)
    Timestamp      = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.User)


class Bad_Acters(models.Model):
    Reporty    = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    Reported   = models.ForeignKey('auth.User',null=True,blank=True, on_delete=models.CASCADE, related_name = 'reported')
    Message    = models.CharField(null=True,blank=True, max_length=500)
    Staff      = models.CharField(null=True,blank=True, max_length=500)
    Timestamp  = models.DateTimeField(auto_now_add=True)     
    def __str__(self):
        return str(self.Reporty)



