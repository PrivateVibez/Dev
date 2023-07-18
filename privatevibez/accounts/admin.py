from django.contrib import admin

# Register your models here.
from .models import * 

admin.site.register(User_Status)
admin.site.register(User_Data)
admin.site.register(Bad_Acters)

