from django.utils.html import format_html
from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import ProductModel, CategoryModel, PhotoProductModel
from main.variables import DECIMAL_PLACES_FIELD, MAX_DIGITS_FIELD, choices_status, StatusProductEnum
# Register your models here.

@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['user_owner', 'name', 'price', 'category', 'status']
    ordering      = ['user_owner']
    list_filter   = ['user_owner', 'status', 'category', 'status']
    search_fields = ['user_owner__name', 'name', 'model']
    readonly_fields = ['user_owner', 'name', 'description', 'category', 'price', 'model', 'dimension', 'weight', 'visualizar_img']
    
    def visualizar_img(self, obj):
        
        imgs = [ f"<img src='{x.photo.url}' />" for x in obj.photoproductmodel_set.all() ]
        
        return format_html('<br>'.join(imgs))


@admin.register(PhotoProductModel)
class PhotoProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'photo', 'active']
    list_filter = ['product', 'active']
    