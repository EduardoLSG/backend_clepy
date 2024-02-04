from django.contrib import admin
from .models import ProductModel, CategoryModel, PhotoProductModel
# Register your models here.


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['user_owner', 'name', 'status', 'price', 'category', 'new']
    ordering      = ['user_owner']
    list_filter   = ['user_owner', 'status', 'category']
    search_fields = ['user_owner__name', 'name', 'model']


@admin.register(PhotoProductModel)
class PhotoProductAdmin(admin.ModelAdmin):
    list_display = ['photo', 'product', 'active']
    list_filter = ['product', 'active']
    