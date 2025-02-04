from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import *
from django.core.files import File
from django.core.files.base import ContentFile

class ChatConsumer(AsyncWebsocketConsumer):
    async def add_group(self,chatroom_id):
        await self.channel_layer.group_add(
                'chat_%s'% chatroom_id,
                self.channel_name
            )

    async def remove_group(self,chatroom_id):
        await self.channel_layer.group_discard(
                'chat_%s'% chatroom_id,
                self.channel_name
            )


    async def handle_chat_notification(self, data):
        room_id=data['groupid']
        username=data['username']
        operation=data['operation']
        return await self.channel_layer.group_send(
            'chat_notification',
            {
                'type': 'chat_notification_method',
                'room_id': room_id,
                'username' : username,
                'operation' : operation
            }
        )

    async def chat_notification_method(self, event):
        # Send message to WebSocket
        username = event['username']
        room_id=event['room_id']
        operation=event['operation']
        if username==self.scope["user"].username:
            if operation=='add':
                await self.add_group(chatroom_id=room_id)
            else:
                await self.remove_group(chatroom_id=room_id)

            json_msgs={
                'message': {
                    'type':'notification',
                    'room_id':room_id
                }
            }
            await self.send(text_data=json.dumps(json_msgs))



    async def add_new_msg(self, data):
        msg=data['message_content']
        user=self.scope["user"]
        is_file=data["is_file"]
        chatroom_id=data["chatroom"]
        if chatroom_id==-1:
            receiver=data['receiver']
            cr=ChatRoom.objects.create()
            user2=User.objects.get(username=receiver)
            cr.roomie.add(user)
            cr.roomie.add(user2)
            cr.save()
            chatroom_id=cr.id
            await self.add_group(chatroom_id=chatroom_id)
            text_data_json={
                'type':'chat_notification',
                'username':user2.username,
                'operation':'add',
                'groupid':chatroom_id
                }
            await self.handle_chat_notification(data=text_data_json)
        # Join room group
        self.chatroom=ChatRoom.objects.filter(id=chatroom_id).first()
        msg_inst=messages.objects.create(auther=user,content=msg,room=self.chatroom)
        if is_file:
            self.session={
                'file_name':data["file_name"],
                'file_size':data["file_size"],
                'upload_status':data["upload_status"],
                'chatroom_id':chatroom_id,
                'messege_id':msg_inst.id
            }
            # Send message to room group
        else:
            return await self.channel_layer.group_send(
                'chat_%s' % chatroom_id,
                {
                    'type': 'chat_message',
                    'message': self.josonify(msg_inst),
                }
            )

    async def uploadFile(self,file_content):
        try:
            msg_inst=messages.objects.get(id=self.session['messege_id'])
            file_name=self.session['file_name']
            chatroom_id=self.session['chatroom_id']
            content=ContentFile(file_content)
            msg_inst.file_msg.save(file_name,content,save=True)
            self.session={}
            return await self.channel_layer.group_send(
                'chat_%s' % chatroom_id,
                {
                    'type': 'chat_message',
                    'message': self.josonify(msg_inst),
                }
            )
        except:
            print('got an error')

    def josonify( self, msg_inst):
        return{
            'id':msg_inst.id,
            'auther': msg_inst.auther.username,
            'room_id': msg_inst.room.id,
            'content': msg_inst.content,
            'file_msg_url':  msg_inst.file_msg.url if msg_inst.file_msg else '',
            'timestamp': msg_inst.timestamp.strftime('%Y-%m-%d %H:%M'),
            'type':'message'
        }
        

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        json_msgs={
            'message': event['message']
        }
        await self.send(text_data=json.dumps(json_msgs))


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='chat_'
        crs=User.objects.get(username=self.room_name).roommate.all()
        for cr in crs:
            await self.add_group(chatroom_id=cr.id)
        await self.add_group(chatroom_id='notification')
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        crs=User.objects.get(username=self.room_name).roommate.all()
        for cr in crs:
            await self.remove_group(chatroom_id=cr.id)
        await self.remove_group(chatroom_id='notification')

    # Receive message from WebSocket
    async def receive(self, text_data=None,bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            if text_data_json['type']=='chat_notification':
                await self.handle_chat_notification(data=text_data_json)
            else:
                await self.add_new_msg(data=text_data_json)
        if bytes_data:
            print('bytes_data')
            await self.uploadFile(file_content=bytes_data)


