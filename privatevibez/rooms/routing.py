from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/user_visitors/(?P<room_id>\d+)/$', consumers.UserVisitorsConsumer.as_asgi()),
    re_path(r'ws/block_countries/(?P<room_id>\d+)/$', consumers.BlockedCountriesConsumer.as_asgi()),

]