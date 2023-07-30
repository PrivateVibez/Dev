from django.urls import path
from . import views
urlpatterns = [
    path('<str:Broadcaster>', views.Room, name="room"),
    path('Menu_item/', views.Menu_item, name="Menu_item"),
    path('Dice_items/', views.Dice_items, name="Dice_items"),
    path('Following/', views.Following, name="Following"),
    path('Thumbs/', views.Thumb, name="Thumb"),
    path('PrivateChatCheckBox/', views.PrivateChatCheckBox, name="PrivateChatCheckBox"),
    path('Chat/', views.Chat, name="Chat"),
    path('Save_RoomPatterns/', views.Save_RoomPatterns, name="Save_RoomPatterns"),
    path('go_online/', views.go_online, name="go_online"),
    path('go_offline/', views.go_offline, name="go_offline"),
    path('fav_btn_trigger_toy/', views.fav_btn_trigger_toy, name="fav_btn_trigger_toy"),
    path('invite_private_chat/', views.invite_private_chat, name="invite_private_chat"),
    path('get_invitees/', views.get_invitees, name="get_invitees"),
    path('accept_privatechat/', views.accept_privatechat, name="accept_privatechat"),
    path('block_countries/', views.block_countries, name="block_countries"),
    path('set_slot_machine/', views.set_slot_machine, name="set_slot_machine"),
    path('deduct_vibez/<int:vibez>', views.deduct_vibez, name="deduct_vibez"),
    path('get_prize/', views.get_prize, name="get_prize"),
    path('lovense/generate_broadcaster_qrcode/', views.generate_broadcaster_qrcode, name="generate_broadcaster_qrcode"),
    
    
]