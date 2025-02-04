from rest_framework import serializers
from .models import *
from chatter.serializers import *

class ChatRoomSerializer(serializers.Serializer):
    link=serializers.CharField()
    timestamp=serializers.DateTimeField()
    name=serializers.CharField()
    img_link=serializers.CharField()
    is_group=serializers.BooleanField()

class MessagesChatroomSerializer(serializers.Serializer):
    auther_name=serializers.CharField()
    sender=serializers.CharField()
    time_stamp=serializers.DateTimeField()
    content=serializers.CharField()
    file_msg_link=serializers.CharField()


class messagesSerializer(serializers.ModelSerializer):
    auther=UserSerializer()
    class Meta:
        model=messages
        fields='__all__'

class ChatRoomSerializerApi(serializers.ModelSerializer):
    messages=MessagesChatroomSerializer(many=True)
    roomie=UserSerializer(many=True)
    room_image_url=serializers.CharField()
    guest_name=serializers.CharField()

    class Meta:
        model=ChatRoom
        fields=[
            'roomie',
            'group',
            'lastping',
            'messages',
            'lastmsg',
            'room_image_url',
            'guest_name',
            'id'
        ]

class profileSerializer(serializers.Serializer):
    username=serializers.DateTimeField()
    name=serializers.CharField()
    email=serializers.CharField()
    img_link=serializers.CharField()
    status=serializers.CharField()
    is_group=serializers.BooleanField()
    members=userSubStrSerializer(many=True)
