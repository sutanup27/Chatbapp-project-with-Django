from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.contrib.auth.models import  User
from .serializers import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

class UserViewsets(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer

@login_required(login_url='/')
def userSubStrApi(request,username_substr=None):
    if username_substr:
        users=[]
        for user in User.objects.filter(Q(username__icontains=username_substr) | Q(first_name__icontains=username_substr) | Q(last_name__icontains=username_substr) ).exclude(username=request.user.username):
            img_link=user.profile.profile_image.url
            users.append({
                'full_name': user.first_name+' '+user.last_name,
                'username': user.username,
                'img_link': img_link
            }
            )
        serializer=userSubStrSerializer(users,many=True)
    else:
        serializer=userSubStrSerializer([],many=True)
    return JsonResponse(serializer.data, safe=False)


