from django.urls import re_path 
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/staff/$', consumers.StaffConsumer.as_asgi()),
    re_path(r'ws/bad_acters/$', consumers.BadActersConsumer.as_asgi()),
    re_path(r'ws/private_vibez_revenue/$', consumers.PrivateVibezRevenueConsumer.as_asgi())
]