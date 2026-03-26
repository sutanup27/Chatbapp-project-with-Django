from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.contrib.auth.models import User
from .models import *
from django.core.files.base import ContentFile


class ChatConsumer(AsyncWebsocketConsumer):

    async def add_group(self, chatroom_id):
        await self.channel_layer.group_add(
            'chat_%s' % chatroom_id,
            self.channel_name
        )

    async def remove_group(self, chatroom_id):
        await self.channel_layer.group_discard(
            'chat_%s' % chatroom_id,
            self.channel_name
        )

    async def handle_chat_notification(self, data):
        return await self.channel_layer.group_send(
            'chat_notification',
            {
                'type': 'chat_notification_method',
                'room_id': data['groupid'],
                'username': data['username'],
                'operation': data['operation']
            }
        )

    async def chat_notification_method(self, event):
        username = event['username']
        room_id = event['room_id']
        operation = event['operation']

        if username == self.scope["user"].username:
            if operation == 'add':
                await self.add_group(chatroom_id=room_id)
            else:
                await self.remove_group(chatroom_id=room_id)

            await self.send(text_data=json.dumps({
                'message': {
                    'type': 'notification',
                    'room_id': room_id
                }
            }))

    # ---------------- DB HELPERS ---------------- #

    @database_sync_to_async
    def create_chatroom(self, user, receiver):
        user2 = User.objects.get(username=receiver)
        cr = ChatRoom.objects.create()
        cr.roomie.add(user)
        cr.roomie.add(user2)
        cr.save()
        return cr, user2

    @database_sync_to_async
    def get_chatroom(self, chatroom_id):
        return ChatRoom.objects.filter(id=chatroom_id).first()

    @database_sync_to_async
    def create_message(self, user, msg, chatroom):
        return messages.objects.create(
            auther=user,
            content=msg,
            room=chatroom
        )

    @database_sync_to_async
    def get_user_rooms(self, username):
        return list(User.objects.get(username=username).roommate.all())

    @database_sync_to_async
    def save_file(self, message_id, file_name, file_content):
        msg_inst = messages.objects.get(id=message_id)
        content = ContentFile(file_content)
        msg_inst.file_msg.save(file_name, content, save=True)
        return msg_inst

    @database_sync_to_async
    def serialize_message(self, msg_inst):
        return {
            'id': msg_inst.id,
            'auther': msg_inst.auther.username,
            'room_id': msg_inst.room.id,
            'content': msg_inst.content,
            'file_msg_url': msg_inst.file_msg.url if msg_inst.file_msg else '',
            'timestamp': msg_inst.timestamp.strftime('%Y-%m-%d %H:%M'),
            'type': 'message'
        }

    # ---------------- CORE LOGIC ---------------- #

    async def add_new_msg(self, data):
        msg = data['message_content']
        user = self.scope["user"]
        is_file = data["is_file"]
        chatroom_id = data["chatroom"]

        if chatroom_id == -1:
            receiver = data['receiver']

            cr, user2 = await self.create_chatroom(user, receiver)
            chatroom_id = cr.id

            await self.add_group(chatroom_id)

            await self.handle_chat_notification({
                'type': 'chat_notification',
                'username': user2.username,
                'operation': 'add',
                'groupid': chatroom_id
            })

        self.chatroom = await self.get_chatroom(chatroom_id)

        msg_inst = await self.create_message(user, msg, self.chatroom)

        if is_file:
            self.session = {
                'file_name': data["file_name"],
                'file_size': data["file_size"],
                'upload_status': data["upload_status"],
                'chatroom_id': chatroom_id,
                'messege_id': msg_inst.id
            }
        else:
            await self.channel_layer.group_send(
                'chat_%s' % chatroom_id,
                {
                    'type': 'chat_message',
                    'message': await self.serialize_message(msg_inst),
                }
            )

    async def uploadFile(self, file_content):
        try:
            msg_inst = await self.save_file(
                self.session['messege_id'],
                self.session['file_name'],
                file_content
            )

            chatroom_id = self.session['chatroom_id']
            self.session = {}

            await self.channel_layer.group_send(
                'chat_%s' % chatroom_id,
                {
                    'type': 'chat_message',
                    'message': await self.serialize_message(msg_inst),
                }
            )
        except:
            print('file upload error')

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))

    # ---------------- CONNECTION ---------------- #

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        crs = await self.get_user_rooms(self.room_name)

        for cr in crs:
            await self.add_group(chatroom_id=cr.id)

        await self.add_group(chatroom_id='notification')
        await self.accept()

    async def disconnect(self, close_code):
        crs = await self.get_user_rooms(self.room_name)

        for cr in crs:
            await self.remove_group(chatroom_id=cr.id)

        await self.remove_group(chatroom_id='notification')

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            data = json.loads(text_data)

            if data['type'] == 'chat_notification':
                await self.handle_chat_notification(data)
            else:
                await self.add_new_msg(data)

        if bytes_data:
            await self.uploadFile(bytes_data)