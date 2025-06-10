from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"^ws/board-update/(?P<board>\d+)/?$",
        consumers.BoardUpdateConsumer.as_asgi(),
    ),
]
