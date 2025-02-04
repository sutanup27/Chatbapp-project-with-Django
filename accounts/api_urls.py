from django.urls import path, include
from .views import *
from rest_framework import routers


urlpatterns = [
    path('Contact/', ContactsApi),
    path('login/', login),
    path('profileapi/',ProfileApi.as_view())
    ]