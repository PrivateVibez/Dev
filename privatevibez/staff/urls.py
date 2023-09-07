
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="staff_home"),
    
    # url for accepting broadcaster or rejecting broadcaster
    path('idStatus/', views.Id_Status, name="Id_Status"),
    
    #url for adding decline messages
    path('addDeclineMsg/', views.addDeclineMsg, name="addDeclineMsg"),
    
    #url for creating staff
    path('createStaff/', views.Create_Staff, name="Create_Staff"),
    
    #url for editing staff permissions
    path('editStaffPermission/', views.editStaffPermission, name="editStaffPermission"),
    
    #url for sending of invitations for staff
    path('sendStaffInvitation/', views.sendStaffInvitation, name="sendStaffInvitation"),
    
    #url for staff registration
    path('staffRegistration/', views.staffRegistration, name="staffRegistration"),
    
    
    
    path('AddDevProject/', views.Add_Dev_Project, name="Add_Dev_Project"),
    path('AddDevList/', views.Add_Dev_List, name="Add_Dev_List"),
    
    #url for fetching staff permissions
    path('getPermission/', views.getPermission, name="getPermission"),
    
    #url for fetching staff information
    path('getStaffInformation/', views.getStaffInformation, name="getStaffInformation"),
    
    #url for deleting staff
    path('deleteStaff/', views.deleteStaff, name="deleteStaff"),
    
    #url for fetching staff messages
    path('getstaffmessages/', views.getstaffmessages, name="getstaffmessages"),
    
    
    path('save_memo/', views.save_memo, name="save_memo"),
    
    #url for pending broadcasters
    path('getPendingBroadcasters/', views.getPendingBroadcasters, name="getPendingBroadcasters"),
    
    
    # approve a pending broadcaster
    path('approveBroadcaster/', views.approveBroadcaster, name="approveBroadcaster"),
    
    # update staff data
    path('updateStaffData/', views.updateStaffData, name="updateStaffData"),
    
    
    # update subscription
    path('update-subscription/', views.updateSubscriptions, name="updateSubscriptions"),
    
    # delete subscription
    path('delete-subscription/', views.deleteSubscriptions, name="deleteSubscriptions"),
    
    
    # update slot machine cost per spin
    path('update_slot_machine_cost_per_spin/', views.update_slot_machine_cost_per_spin, name="update_slot_machine_cost_per_spin"),
    
    # add promotion
    path('save_Promotion/', views.save_Promotion, name="save_Promotion"),
    
    # update promotion
    path('update_Promotion/', views.update_Promotion, name="update_Promotion"),
    
    # delete promotion
    path('delete_Promotion/<int:id>/', views.delete_Promotion, name="delete_Promotion"),
    
    # send promotion
    path('send_Promotion/', views.send_Promotion, name="send_Promotion")
]
