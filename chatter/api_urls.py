from django.urls import path, include
from .views import *
from rest_framework import routers


router=routers.DefaultRouter()
router.register('',UserViewsets)

urlpatterns = [
    path('User', include(router.urls)),
    path('findusers/<str:username_substr>', userSubStrApi),
    path('findusers/', userSubStrApi)
    ]