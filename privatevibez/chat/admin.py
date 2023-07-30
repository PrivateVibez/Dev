from django.contrib import admin
from .models import * 


class PublicAdmin(admin.ModelAdmin):
    list_display = ('User', 'Room', 'Message', 'Timestamp')
    list_display_links = ('User', 'Room', 'Message', 'Timestamp')
    list_per_page = 30

admin.site.register(Public, PublicAdmin)

class PrivateAdmin(admin.ModelAdmin):
    list_display = ('From', 'To', 'Message', 'Timestamp')
    list_display_links = ('From', 'To', 'Message', 'Timestamp')
    list_per_page = 30


class StaffAdmin(admin.ModelAdmin):
    list_display = ('From', 'To', 'Message', 'Timestamp')
    list_display_links = ('From', 'To', 'Message', 'Timestamp')
    list_per_page = 30
    
    
class Private_Chat_InviteeAdmin(admin.ModelAdmin):
    list_display = ('broadcaster',)
    list_display_links = ('broadcaster',)
    list_per_page = 30
    
admin.site.register(Staff, StaffAdmin)
admin.site.register(Private, PrivateAdmin)
admin.site.register(PrivateRoomManager)
admin.site.register(Private_Chat_Invitee,Private_Chat_InviteeAdmin)