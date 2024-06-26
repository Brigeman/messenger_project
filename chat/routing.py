from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/group/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(
        r"ws/chat/private/(?P<user_id>\d+)/$", consumers.PrivateChatConsumer.as_asgi()
    ),
]
