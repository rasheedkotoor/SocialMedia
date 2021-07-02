import base64
import json

from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile

from accounts.models import User
from student.models import Message, Room


class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):  # join group
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):  # leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):  # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        message_type = text_data_json['message_type']
        user1_id = text_data_json['user1']
        user2_id = text_data_json['user2']

        room = Room.objects.get(room_name=self.room_name)
        user1 = User.objects.get(id=user1_id)
        user2 = User.objects.get(id=user2_id)
        if message_type == 'text':
            text = message
            file = ''
        else:
            inp_file = message
            format, imgstr = inp_file.split(';base64,')
            ext = format.split('/')[-1]
            file = ContentFile(base64.b64decode(imgstr), name=user1.username + '.' + ext)
            text = ''

        Message.objects.create(room=room, user1=user1, message_type=message_type, user2=user2, message=text,
                               vid_img=file)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
                'message_type': message_type,
            }
        )

    def chatroom_message(self, event):  # Send message to WebSocket
        message = event['message']
        username = event['username']
        message_type = event['message_type']

        async_to_sync(self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'message_type': message_type,
        })))


# class ChatRoomConsumer(AsyncWebsocketConsumer):
#     async def connect(self):  # join group
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()
#
#     async def disconnect(self, close_code):  # leave group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     async def receive(self, text_data=None, bytes_data=None):  # Receive message from WebSocket
#         text_data_json = json.loads(text_data)
#         # print('-----------------------------------------------------------------')
#         # print(text_data)
#         message = text_data_json['message']
#         username = text_data_json['username']
#         user1 = text_data_json['user1']
#         user2 = text_data_json['user2']
#         room_name = self.room_name
#         room = Room.objects.get(room_name=room_name)
#         # print(message, username, user2, user1, room_name, '[][][][][][][][][][][][][][][][][][')
#         # print(self.user_id)
#         await self.save_message(self, '4', user1, user2, message)
#
#         await self.channel_layer.group_send(
#             # print('-----------------------------------------------------------------'),
#             # print(text_data),
#             self.room_group_name,
#             {
#                 'type': 'chatroom_message',
#                 'message': message,
#                 'username': username,
#             }
#         )
#
#     @database_sync_to_async
#     def save_message(self, message, user1, user2, room):
#         obj = Message.objects.create(room=room, user1=user1, user2=user2, message=message)
#         obj.save()
#         # print(obj)
#         return obj
#
#     async def chatroom_message(self, event):  # Send message to WebSocket
#         message = event['message']
#         username = event['username']
#
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'username': username,
#         }))
#
#     pass
