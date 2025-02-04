from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Contacts, Profile
from chat.models import ChatRoom
from django.http import HttpResponse, JsonResponse
from .serializers import *
from rest_framework.decorators import api_view
import json
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework import viewsets, generics, views
from rest_framework.response import Response

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1!=password2 :
            messages.info(request,"Password doesn't match.")
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request,"User Name is taken. Please try some other name.")
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,"This E-mail id is already in use. Please try something else.")
            return redirect('register')
        else :
            auth.logout(request)
            user=User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name, email=email)
            Profile.objects.create(host=user)
            return redirect('/')
    else :
        return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        if not User.objects.filter(username=username).exists():
            messages.info(request,"User Name doesn't exists.")
            return redirect('/')
        else:
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('/')
            else:
                messages.error(request,'Username or password invallid')
                return redirect('/')
    else:
        return render(request,'home.html')

def logout(request) :
    auth.logout(request)
    return redirect('/')

@login_required(login_url='/')
def contacts(request) :
    cntcs=Contacts.objects.filter(host=request.user).order_by('first_name','last_name')
    contacts=[]
    for cntc in cntcs:
        img_link=User.objects.filter(username=cntc.username).first().profile.profile_image.url
        contacts.append(
            {
                'full_name':cntc.first_name+' '+cntc.last_name,
                'username': cntc.username,
                'img_link':img_link
            }
        )
    return render(request,'contacts.html',{'contacts':contacts})

@login_required(login_url='/')
def add_contacts(request) :
    return render(request,'add_contact.html')

@login_required(login_url='/')
def add_contact(request) :
    if request.method == 'GET':
        first_name=request.GET['first_name']
        last_name=request.GET['last_name']
        username=request.GET['username']
        if User.objects.filter(username=username).exclude(username=request.user.username).exists():
            Contacts.objects.create(host=request.user, first_name=first_name, last_name=last_name, username=username)
            return redirect('contacts')
        else:
            messages.info(request,"User Name doesn't exits.")   
            return redirect('add_contacts')
    else:
        return redirect('contacts')
        

@login_required(login_url='/')
def create_group(request):
    contacts=Contacts.objects.filter(host=request.user).order_by('first_name','last_name')
    return render(request,'create_group.html',{'contacts':contacts})

def add_users_chatroom(Chatroom,contacts):
    for contact in contacts:
        user=User.objects.get(username=contact)
        Chatroom.roomie.add(user)
    Chatroom.save()


@login_required(login_url='/')
def add_group(request):
    if request.method == 'POST':
        group_name=request.POST['group_name']
        contacts=request.POST.getlist('contact[]')
        Chatroom=ChatRoom.objects.create(group=True,group_name=group_name)
        Chatroom.roomie.add(request.user)
        add_users_chatroom(Chatroom=Chatroom,contacts=contacts)
        return render(request,'home.html')
    else:
        return redirect('contacts')



@login_required(login_url='/')
def add_group_user(request,room_id):
    Chatroom=ChatRoom.objects.filter(id=room_id).first()
    existng_roommates=[ x.username for x in Chatroom.roomie.all()]
    contacts=Contacts.objects.filter(host=request.user).exclude(username__in=existng_roommates).order_by('first_name','last_name')
    return render(request,'add_group_user.html',{'contacts':contacts, 'room_id':room_id, 'room_name':Chatroom.group_name})


@login_required(login_url='/')
def add_users_to_group(request):
    if request.method == 'POST':
        room_id=request.POST['room_id']
        contacts=request.POST.getlist('contact[]')
        Chatroom=ChatRoom.objects.filter(id=room_id)
        if Chatroom.exists():
            add_users_chatroom(Chatroom=Chatroom.first(),contacts=contacts)
            return redirect('chatroom',room_id=Chatroom.first().id)
        else:
            print('room does not exists')
    else:
        return redirect('contacts')

@login_required(login_url='/')
def profile(request):
    render (request,'profile')

@login_required(login_url='/')
@api_view(['GET', 'POST'])    
def ContactsApi(request) :
    usr=request.user
    if request.method == 'GET':
        cntcs=Contacts.objects.filter(host=usr).order_by('first_name','last_name')
        contacts=[]
        for cntc in cntcs:
            if User.objects.filter(username=cntc.username).first():
                img_link=User.objects.filter(username=cntc.username).first().profile.profile_image.url
            else:
                img_link=''
            contacts.append(
                {
                    'full_name':cntc.first_name+' '+cntc.last_name,
                    'username': cntc.username,
                    'room_image_url': img_link
                }
            )
        try:
            room_id=request.GET['roomid']
            room=ChatRoom.objects.filter(id=room_id).first()
            roommate=[ roomie.username for roomie in room.roomie.all()]
            contacts=[ contact for contact in contacts if contact['username'] not in roommate ]
            serializer=ContactsSerializer(contacts,many=True)
            return JsonResponse(serializer.data, safe=False)
        except:
            serializer=ContactsSerializer(contacts,many=True)
            return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        first_name=request.data['first_name']
        last_name=request.data['last_name']
        username=request.data['username']
        if User.objects.filter(username=username).exclude(username=request.user.username).exists():
            Contacts.objects.create(host=request.user, first_name=first_name, last_name=last_name, username=username)
            return JsonResponse({'message':'Contact has been Created'}, safe=False)
        else:
            return JsonResponse({'message': 'user with {} not exist'.format(username)}, status=404)
    else:
        pass




class ProfileApi(views.APIView) :
    parser_class = (FileUploadParser,)

    def get(self, request,format=None):
        usr=request.user
        profile=Profile.objects.filter(host=usr).first()
        serializer=ProfileSerializerApi(profile)
        return Response(serializer.data)

    def put(self, request ):
        usr=request.user
        data=json.loads(request.data['data'])
        instance=Profile.objects.filter(host=usr).first()
        if instance:
            serializer=ProfileSerializerApi(instance,data=data , partial=True)
            if serializer.is_valid():
                try:
                    image=request.data['image']
                    instance.profile_image.save(image.name,image,save=True)
                except:
                    pass
                serializer.save()
                return Response(serializer.data,status=200)
            else:
                return Response(serializer.errors,status=400)
        else:
            return Response({'message':'profile doesnot extsts'}, status=400)


