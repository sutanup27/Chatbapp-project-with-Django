from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.register , name='register'),
    path('login', views.login , name='login'),
    path('logout', views.logout , name='logout'),
    path('contacts', views.contacts , name='contacts'),
    path('create_group', views.create_group , name='create_group'),
    path('add_group', views.add_group , name='add_group'),
    path('add_users_to_group', views.add_users_to_group , name='add_users_to_group'),
    path('add_group_user_<str:room_id>', views.add_group_user , name='add_group_user'),
    path('add_contacts', views.add_contacts , name='add_contacts'),
    path('add_contact', views.add_contact , name='add_contact'),
]
