from django.contrib import admin
from .forms import *
from .models import *

from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(UserModel)
class UserAdmin(UserAdmin):
    ordering = ['name']
    list_display = ['name', 'email', 'phone', 'type_doc','document', 'terms_accept']
    list_filter  = ['type_doc']    
    search_fields = ['name', 'email', 'phone', 'document']
    readonly_fields = ['document', 'type_doc', 'terms_accept',  'date_joined', 'last_login']
    
    add_fieldsets = (
        ('Informações ', {'fields': ('email', 'password', 'name', 'phone', 'type_doc', 'document', 'photo_profile')}),
    )
    fieldsets =  add_fieldsets + (
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )

    readonly_fields = ('date_joined', )
    
    form     = UserUpdateForm
    add_form = UserRegisterForm
    
@admin.register(LocalizationUserModel)
class LocalizatiionUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'state', 'city', 'district', 'street', 'number', 'postal_code']