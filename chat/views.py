from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import *
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import viewsets, generics, views
from django.http import HttpResponse, JsonResponse
from .models import *
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

# Create your views here.
@login_required(login_url='')
def chat(request):
    usr=request.user
    chatrooms=[]
    for Chatroom in ChatRoom.objects.filter(roomie=usr):
        guest_name=Chatroom.guest_name(usr)
        img_link=Chatroom.room_image(usr)
        link=Chatroom.id
        chatrooms.append({
            'link':link,
            'name':guest_name,
            'timestamp':Chatroom.lastping.strftime('%Y-%m-%d %H:%M'),
            'img_link': img_link
        })
    Chatrooms=sorted(chatrooms, key=lambda x: x['timestamp'], reverse = True)
    return render(request,'chat.html',{'chatrooms': Chatrooms})

@login_required(login_url='/')
def chatroom(request, room_id):
    room=ChatRoom.objects.filter(id=room_id,roomie=request.user)
    if room.exists():
        return render(request,'chatroom.html',{'room_id':room_id, 'room_type':room.first().group, 'room_name':room.first().guest_name(request.user) })
    else:
        raise PermissionDenied("You do not have permission")

def get_room(user):
    prof=user.profile
    return {
        'full_name':user.first_name+' '+user.last_name,
        'username':user.username,
        'img_link': prof.profile_image.url
        }


def get_create_room(user1,user2):
    if user1==user2:
        return None
    chatroom1=user1.roommate.filter(group=False)
    chatroom2=user2.roommate.filter(group=False)
    chatroom=set(chatroom2).intersection(chatroom1)
    if chatroom!=set():
        return chatroom.pop()
    else:
        Chatroom=ChatRoom.objects.create(group=False)
        Chatroom.roomie.add(user1,user2)
        Chatroom.save()
        return Chatroom

@login_required(login_url='/')
def get_or_create_room(request,username):
    user1=request.user
    user2=User.objects.filter(username=username).first()
    chatroom=get_create_room(user1=user1,user2=user2)
    return redirect('chatroom',room_id=chatroom.id)

@login_required(login_url='/')
def search_name(request):
    if request.method == 'GET':
        username_substring=request.GET['username_substring']
        users=[]
        for user in User.objects.filter(username__icontains=username_substring).exclude(username=request.user.username):
            img_link=user.profile.profile_image.url
            users.append({
                'full_name': user.first_name+' '+user.last_name,
                'username': user.username,
                'img_link': img_link
            }
            )
        return render(request,'search.html',{'users':users})
    else :
        return redirect('search')

@login_required(login_url='/')
def search(request):
        return render(request,'search.html',{'users':[]})


# class ChatRoomView(generics.ListAPIView):
#     serializer_class=ChatRoomSerializer

#     def get_queryset(self):
#         queryset=ChatRoom.objects.all()
#         host=self.request.query_params.get("host",'')
#         if host:
#             host_user=User.objects.get(username=host)
#             return queryset.filter(roomie=host_user)
#         return queryset



@login_required(login_url='/')
def chatroomMessageViewApi(request):
    roomid=request.GET['roomid']
    messages=[]
    if roomid:
        room=ChatRoom.objects.filter(id=roomid).first()
        for msg in room.messages:
            is_send=False
            file_url=''
            auther_name=msg.auther.username
            if auther_name==request.user.username:
                is_send=True
            else:
                c_name=request.user.host.filter(username=auther_name).first()
                if c_name:
                    auther_name=c_name.full_name
            if msg.file_msg:
                file_url=msg.file_msg.url
            messages.append({
                "content":msg.content,
                "file_msg_link":file_url,
                "time_stamp":msg.timestamp.strftime('%Y-%m-%d %H:%M'),
                "auther_name":auther_name,
                "sender": msg.auther
            })

    serializer=MessagesChatroomSerializer(messages,many=True)
    return JsonResponse(serializer.data, safe=False)

def jsonify_room(Chatroom,usr):
    guest_name=Chatroom.guest_name(usr)
    img_link=Chatroom.room_image(usr)
    link=Chatroom.id
    return {
        'link':link,
        'name':guest_name,
        'timestamp':Chatroom.lastping.strftime('%Y-%m-%d %H:%M'),
        'img_link': img_link,
        'is_group':Chatroom.group
        }



@login_required(login_url='/')
def chatRoomsApi(request,username=''):
    usr=request.user
    if username:
        user2=User.objects.filter(username=username).first()
        chatroom=get_create_room(user1=usr,user2=user2)
        serializer=ChatRoomSerializer(jsonify_room(chatroom,usr))
        return JsonResponse(serializer.data, safe=False)

    chatrooms=[ jsonify_room(Chatroom,usr)  for Chatroom in ChatRoom.objects.filter(roomie=usr)]
    Chatrooms=sorted(chatrooms, key=lambda x: x['timestamp'], reverse = True)
    serializer=ChatRoomSerializer(Chatrooms,many=True)
    return JsonResponse(serializer.data, safe=False)

class messagesViewapi(views.APIView):
    def get(self, request, id=None):
        if id:
            msgs=messages.objects.get(id=id)
            serializer=messagesSerializer(msgs)
            return Response(serializer.data)

        msgs=messages.objects.all()
        serializer=messagesSerializer(msgs,many=True)
        return Response(serializer.data)

    def post(self, request, id=None):
        user=request.data



class chatroomsViewapi(views.APIView):
    def get(self, request,id=None):
        usr=request.user
        chatrooms=[]
        if id:
            cr=ChatRoom.objects.get(id=id)
            chatroom={
                        'roomie': cr.roomie,
                        'group': cr.group,
                        'lastping':cr.lastping,
                        'messages':cr.messages,
                        'lastmsg':cr.lastmsg,
                        'room_image_url':cr.room_image(usr),
                        'guest_name':cr.guest_name(usr),
                        'id':cr.id
                    }
            serializer=ChatRoomSerializerApi(chatroom)
            return Response(serializer.data)

        for cr in usr.roommate.all():
            chatrooms.append(
                {
                    'roomie': cr.roomie,
                    'group': cr.group,
                    'lastping':cr.lastping,
                    'messages':cr.messages,
                    'lastmsg':cr.lastmsg,
                    'room_image_url':cr.room_image(usr),
                    'guest_name':cr.guest_name(usr),
                    'id':cr.id
                }
            )

        Chatrooms=sorted(chatrooms, key=lambda x: x['lastping'], reverse = True)
        serializer=ChatRoomSerializerApi(Chatrooms,many=True)
        return Response(serializer.data)

    def put(self, request, id=None):
        instance=ChatRoom.objects.get(id=id)
        try:
            username=request.data['newroomie']
            user=User.objects.filter(username=username).first()
            if user:
                instance.roomie.add(user)
                instance.save()
                return Response({ 'status': 'new user is added'},status=200)
            else:
                return Response(serializer.errors,status=400)
        except:
            data=request.data
            serializer=ChatRoomSerializerApi(instance,data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=200)
            return Response(serializer.errors,status=400)

    def post(self, request):
        try:
            user=request.user
            group_name=request.data['group_with_current_user']
            new_roomies=request.data['added_contacts']
            instance=ChatRoom.objects.create(group=True,group_name=group_name)
            instance.roomie.add(user)
            for roommate in new_roomies:
                print(roommate)
                new_user=User.objects.get(username=roommate)
                instance.roomie.add(new_user)
            instance.save()
            return Response({'message':'Group has been Created'},status=200)
        except:
            if group_name:
                return Response({ 'message': 'Chatroom has not been created'},status=400)
            data=request.data
            serializer=ChatRoomSerializerApi(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=200)
            return Response(serializer.errors,status=400)

@login_required(login_url='/')
def profileView(request,room_id='') :
    profile=[]
    usr=request.user
    if room_id :
        cr=ChatRoom.objects.filter(id=room_id).first()
        if cr:
            roomie=cr.roomie.all()
            opponent=roomie.exclude(username=usr.username).first()
            username= '' if cr.group else opponent.username
            name=cr.guest_name(usr)
            email= '' if cr.group else opponent.email
            img_link=cr.room_image(usr)
            is_group= cr.group
            members= [ get_room(roommate) for roommate in roomie] if cr.group else []
            status= '' if cr.group else opponent.profile.status
    else :
        username=usr.username
        name=usr.first_name+' '+usr.last_name
        email= usr.email
        img_link=usr.profile.profile_image.url
        is_group= False
        members= []
        status=usr.profile.status

    profile={
    'username':username,
    'name':name,
    'email':email,
    'img_link':img_link,
    'is_group':is_group,
    'members':members,
    'status':status
    }
    serializer=profileSerializer(profile)
    return JsonResponse(serializer.data, safe=False)
