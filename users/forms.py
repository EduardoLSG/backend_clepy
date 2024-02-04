from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ['name','email', 'phone', 'document',  'password1', 'password2', 'is_superuser', 'is_staff', 'photo_profile']
        
        
class UserUpdateForm(UserChangeForm):

    class Meta:
        model = UserModel
        fields = ('name', 'email', 'phone', 'is_superuser', 
                  'is_staff', 'is_active', 'photo_profile', 
                  'groups')
        
        
        
