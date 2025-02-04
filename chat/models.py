from django.db import models
from accounts.models import Contacts,Profile
from django.contrib.auth.models import auth, User
from django.contrib import admin
from django.utils import timezone
import uuid 

# Create your models here.


class ChatRoom(models.Model):
    roomie=models.ManyToManyField(User,related_name='roommate', symmetrical=True, blank=True )
    group=models.BooleanField(default=False)	
    group_name=models.TextField(null=True)
    create_datetime=models.DateTimeField(auto_now_add=True)
    group_image=models.ImageField(upload_to='accounts/images/', default='accounts/images/default_group_image.png')

    @property
    def lastping(self):
        msg=messages.objects.filter(room=self).order_by('-timestamp')
        if msg.exists():
            return msg.first().timestamp
        else:
            return self.create_datetime

    @property
    def lastmsg(self):
        msg=messages.objects.filter(room=self).order_by('-timestamp')
        if msg.exists():
            return msg.first().content
        else:
            return ''

    @property
    def messages(self):
        msgs=[]
        for msg in self.room_message.all().order_by('timestamp'):
            msgs.append(
                {
                "content":msg.content,
                "file_msg_link": msg.file_msg.url if msg.file_msg  else '',
                "time_stamp":msg.timestamp.strftime('%Y-%m-%d %H:%M'),
                "auther_name":msg.auther.first_name+' '+msg.auther.last_name,
                "sender":msg.auther
                }
            )
        return msgs


    def guest_name(self,user):
        if self.group:
            return self.group_name
        else:
            guest=self.roomie.exclude(username=user.username).first()
            contact=Contacts.objects.filter(host=user,username=guest.username)
            if contact.exists():
                return contact.first().first_name+' '+contact.first().last_name
            else:
                return guest.username

    def room_image(self,user):
        if self.group:
            return self.group_image.url
        else:
            guest=self.roomie.exclude(username=user.username).first()
            guest_profile=guest.profile
            return guest_profile.profile_image.url

    def __str__(self):
        return str(self.id)

 

admin.site.register(ChatRoom)

class messages(models.Model):
    auther=models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg')
    content=models.TextField(blank=True)
    file_msg=models.FileField(upload_to='Chat/files',blank=True)
    file_type=models.TextField(blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    room=models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='room_message')

    def __str__(self):
        return str(self.room.id)+str(self.timestamp)



admin.site.register(messages)