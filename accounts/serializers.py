from rest_framework import serializers
from .models import *
from chatter.serializers import *

class ContactsSerializer(serializers.Serializer):
    username=serializers.DateTimeField()
    full_name=serializers.CharField()
    room_image_url=serializers.CharField()


class ProfileSerializerApi(serializers.ModelSerializer):
    host=UserSerializer()
    class Meta:
        model = Profile
        fields = '__all__'

    def update(self, instance, validated_data):
        host = validated_data.pop('host')
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        first_name=host['first_name']
        last_name=host['last_name']
        email=host['email']
        user=User.objects.get(username=instance.host.username)
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.save()
        return instance


