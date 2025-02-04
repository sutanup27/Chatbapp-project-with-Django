from rest_framework import serializers
from django.contrib.auth.models import  User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=(
            'first_name',
            'last_name',
            'username',
            'email',
            'id'
        )


class userSubStrSerializer(serializers.Serializer):
    username=serializers.CharField()
    full_name=serializers.CharField()
    img_link=serializers.CharField()

