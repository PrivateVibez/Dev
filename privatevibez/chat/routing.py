from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/publicChat/(?P<room_name>[^/]+)/$', consumers.PublicChatConsumer.as_asgi()),
    re_path(r'ws/privateChat/(?P<broc>[^/]+)/(?P<user_name>[^/]+)/$', consumers.PrivateChatConsumer.as_asgi()),
    re_path(r'ws/privateChatBroc/(?P<broc>[^/]+)/(?P<user_name>[^/]+)/$', consumers.PrivateChatConsumerBroc.as_asgi())
]