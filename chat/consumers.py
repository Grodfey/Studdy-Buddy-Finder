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
# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["user"]
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "user": username,
                "message": message
            })

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["user"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "user": username,
            "message": message
            }))