from django.contrib import admin

# Register your models here.
from .models import * 

admin.site.register(Room_Data)
admin.site.register(Room_Sesson)
admin.site.register(Menu_Data)
admin.site.register(Dice_Data)
admin.site.register(Follows)
admin.site.register(Thumbs)
admin.site.register(Room_Visitors)
admin.site.register(Blocked_Regions)
admin.site.register(Blocked_Countries)
