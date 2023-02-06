"""
/***************************************************************************************
*  REFERENCES
*  Title: Tutorial: Implementing a chat server
*  Author: Channels Docs
*  Date: 11/08/2022
*  URL: https://channels.readthedocs.io/en/latest/tutorial/part_1.html
*
*  Title: Tutorial: Implementing a chat server
*
***************************************************************************************/
"""
# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]