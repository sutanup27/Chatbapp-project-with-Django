from django.db import models
from django.contrib.auth.models import auth, User
from django.contrib import admin

# Create your models here.
class Contacts(models.Model):
    host=models.ForeignKey(User, on_delete=models.CASCADE, related_name='host')
    first_name=models.TextField()
    last_name=models.TextField()
    username=models.TextField()
    
    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return self.first_name+' '+self.last_name

admin.site.register(Contacts)

class Profile(models.Model):
    host=models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',primary_key = True)
    profile_image=models.ImageField(upload_to='accounts/images/', default='accounts/images/default_profile_image.png')
    status=models.TextField(blank=True)
    
    def __str__(self):
        return self.host.username

admin.site.register(Profile)

