from django.conf.urls import url
from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
        path('ws/chat/<str:room_name>/', consumers.ChatRoomConsumer.as_asgi()),
        # re_path(r'ws/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
        # url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatRoomConsumer),

]
