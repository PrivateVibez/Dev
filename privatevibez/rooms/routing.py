from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/user_visitors/(?P<room_id>\d+)/$', consumers.UserVisitorsConsumer.as_asgi()),
    re_path(r'ws/room_viewer/(?P<room_id>\d+)/$', consumers.RoomViewersConsumer.as_asgi()),
    re_path(r'ws/blocking/(?P<room_id>\d+)/$', consumers.BlockedCountriesConsumer.as_asgi()),
    re_path(r'ws/user_session/$', consumers.UserSessionConsumer.as_asgi()),

]