from django.urls import path, include
from .views import *
from rest_framework import routers



urlpatterns = [
    path('ChatRoom/<str:username>', chatRoomsApi),
    path('chatroomapi/', chatroomsViewapi.as_view()),
    path('chatroomapi/<int:id>', chatroomsViewapi.as_view()),
    path('ChatRoom/', chatRoomsApi),
    path('messages/', chatroomMessageViewApi),
    path('messagesapi/', messagesViewapi.as_view()),
    path('messagesapi/<int:id>', messagesViewapi.as_view()),
    path('profile/<int:room_id>', profileView),
    path('profile/', profileView),
    ]