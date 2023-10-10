from django.contrib import admin
from cities.models import City, Country, Region
# Register your models here.
from .models import * 

admin.site.register(Room_Data)
admin.site.register(Room_Sesson)
admin.site.register(Menu_Data)
admin.site.register(Dice_Data)
admin.site.register(Follows)
admin.site.register(Thumbs)
admin.site.register(Room_Visitors)
# admin.site.register(City)
# admin.site.register(Country)
# admin.site.register(Region)
# admin.site.register(Blocked_Regions)
# admin.site.register(Blocked_Countries)
admin.site.register(Slot_Machine)
admin.site.register(Games_Data)
admin.site.register(Lottery)
admin.site.register(Social_Media_Links)
admin.site.register(Dice)

