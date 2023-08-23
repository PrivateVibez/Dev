from django.urls import path
from . import views
urlpatterns = [
    # url for broadcaster room
    path('<str:Broadcaster>', views.Room, name="room"),
    
    # url for broadcaster games
    path('save_menu_data/', views.save_menu_data, name="save_menu_data"),
    path('update_menu_data/', views.update_menu_data, name="update_menu_data"),
    path('remove_menu_data/', views.remove_menu_data, name="remove_menu_data"),
    path('avail_menu_item/', views.avail_menu_item, name="avail_menu_item"),
    path('Dice_items/', views.Dice_items, name="Dice_items"),
    
    # url for folowing and liking of broadcaster
    path('Following/', views.Following, name="Following"),
    path('Thumbs/', views.Thumb, name="Thumb"),
    
    # url for broadcaster visitors
    path('visitor/', views.Visitor, name="visitor"),
    
    # urls for enabling private chat and public chat
    path('PrivateChatCheckBox/', views.PrivateChatCheckBox, name="PrivateChatCheckBox"), 
    path('PublicChatCheckBox/', views.PublicChatCheckBox, name="PublicChatCheckBox"), 
    path('Chat/', views.Chat, name="Chat"),
    
    # url for editing favorite button patterns
    path('Save_RoomPatterns/', views.Save_RoomPatterns, name="Save_RoomPatterns"),
    
    #urls for going online and offline broadcasting
    path('go_online/', views.go_online, name="go_online"),
    path('go_offline/', views.go_offline, name="go_offline"),
    
    # urls for triggering favorite buttons
    path('fav_btn_trigger_toy/', views.fav_btn_trigger_toy, name="fav_btn_trigger_toy"),
    
    # urls for user invitation for a private chat
    path('invite_private_chat/', views.invite_private_chat, name="invite_private_chat"),
    
    #urls for getting broadcaster private chat invites
    path('get_invitees/', views.get_invitees, name="get_invitees"),
    
    #url for accepting broadcaster private chat invitees
    path('accept_privatechat/', views.accept_privatechat, name="accept_privatechat"),
    
    # #url for blocked users
    path('404/block_countries/', views.block_countries, name="block_countries"),
    
    # url for setting slot machine
    path('set_slot_machine/', views.set_slot_machine, name="set_slot_machine"),
    
    # url for deducting vibez on purchase of items
    path('deduct_vibez/<int:vibez>', views.deduct_vibez, name="deduct_vibez"),
    
    # url for broadcaster to get the prize from the slot machine
    path('get_prize/', views.get_prize, name="get_prize"),
    
    # fetching broadcaster qr code from lovense api
    path('lovense/generate_broadcaster_qrcode/', views.generate_broadcaster_qrcode, name="generate_broadcaster_qrcode"),
    
    
    # Search Countries
     path('search_countries/', views.search_countries, name="search_countries"),
     path('search_regions/', views.search_regions, name="search_regions"),
     
     #blocked users
     path('blocked/404/', views.user_blocked, name="user_blocked"),
     
     #updating bio
     path('submit_bio/', views.submit_bio, name="submit_bio"),
     
     
    #  updating room rules
     path('update_room_rules/', views.update_room_rules, name="update_room_rules"),
     
     
    #Room Stats
    
         path('hashtags/save', views.save_hashtags, name="save_hashtags"),
     

     

    
    
]