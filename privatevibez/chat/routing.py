from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/publicChat/(?P<room_name>[^/]+)/$', consumers.PublicChatConsumer.as_asgi()),
    re_path(r'ws/privateChat/(?P<broc>[^/]+)/(?P<user_name>[^/]+)/$', consumers.PrivateChatConsumer.as_asgi()),
    re_path(r'ws/privateChatInvitation/(?P<broc>[^/]+)/(?P<user_name>[^/]+)/$', consumers.privateChatInvitation.as_asgi()),
    re_path(r'ws/privateChatBroc/(?P<broc>[^/]+)/(?P<user_name>[^/]+)/$', consumers.PrivateChatConsumerBroc.as_asgi()),
    re_path(r'ws/staffChat/(?P<broc>[^/]+)/(?P<user_name>[^/]+)/$', consumers.StaffChatConsumer.as_asgi()),
    re_path(r'ws/staffChatBroc/(?P<broc>[^/]+)/(?P<user_name>[^/]+)/$', consumers.StaffChatConsumerBroc.as_asgi()),
]