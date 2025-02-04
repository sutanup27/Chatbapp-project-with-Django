from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.chat , name='chat'),
    path('search', views.search , name='search'),
    path('search_name', views.search_name , name='search_name'),
    path('get_or_create_room/<str:username>', views.get_or_create_room , name='get_or_create_room'),
    path('chatroom/<str:room_id>/', views.chatroom , name='chatroom')
]
