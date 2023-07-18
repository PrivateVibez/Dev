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
    
]