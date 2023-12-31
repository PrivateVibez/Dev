from django.urls import path
from . import views

app_name = 'rooms'

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
     path('notfound/404/', views.user_blocked, name="user_blocked"),
     
     #updating bio
     path('submit_bio/', views.submit_bio, name="submit_bio"),
     
     
    #  updating room rules
     path('update_room_rules/', views.update_room_rules, name="update_room_rules"),
     path('update_room_description/', views.update_room_description, name="update_room_description"),
     
     
    #Room Stats
    
         path('hashtags/save', views.save_hashtags, name="save_hashtags"),
         
         
         
         path('get_follower_spending/<str:username>/<str:room>/', views.get_follower_spending, name="get_follower_spending"),
         
         path('get_user_by_date_spending/', views.get_user_by_date_spending, name="get_user_by_date_spending"),
         
         
         path('set_lottery_prize/', views.set_lottery_prize, name="set_lottery_prize"),
         
         path('set_dice_prize/', views.set_dice_prize, name="set_dice_prize"),
         
         
         path('get_lottery_prize/', views.get_lottery_prize, name="get_lottery_prize"),
         
         
        #  Button activation
         path('enable_menu_items/', views.enable_menu_items, name="enable_menu_items"),
         
         path('enable_dice/', views.enable_dice, name="enable_dice"),
         
         path('enable_lottery/', views.enable_lottery, name="enable_lottery"),
         
         
         path('give_dice_price/', views.give_dice_price, name="give_dice_price"),
         
         
         #set social media links
         path('set_social_media_links/', views.set_social_media_links, name="set_social_media_links"),
         
         
         #get social media link
         path('avail_social_media_link/', views.avail_social_media_link, name="avail_social_media_link"),
         
         
         #remove social media link
         path('remove_social_media_link/', views.remove_social_media_link, name="remove_social_media_link"),
         
         #try broadcaster button
         path('try_broadcaster_button/', views.try_broadcaster_button, name="try_broadcaster_button"),
     

     

    
    
]