from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import CategoryModel, ProductModel, PhotoProductModel
from django.contrib.humanize.templatetags.humanize import intcomma

class CategorySerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'
        

class ProductSerializer(ModelSerializer):
    
    images = serializers.SerializerMethodField('get_images', required=False)
    status_display = serializers.CharField(source='get_status_display', required=False)
    user_owner_display = serializers.SerializerMethodField('get_user_owner', required=False)
    price_display = serializers.SerializerMethodField('get_price_currency', required=False)
    category_display = serializers.SerializerMethodField('get_category', required=False)
    
    def get_price_currency(self, obj):
        return intcomma(round(obj.price, 2), True)
    
    def get_images(self, obj):
        photos = PhotoProductModel.objects.filter(product=obj.pk).order_by('order')
        data = []
        for photo in photos:
            data.append({'url': photo.photo.url, 'id': str(photo.id)})
        return data    
    
    def get_user_owner(self, obj):
        return {'id': obj.user_owner.id, 'name': obj.user_owner.name, 'cellphone': obj.user_owner.phone}
    
    def get_category(self, obj):
        return {'id': obj.category.id, 'name': obj.category.name }
    
    class Meta:
        model = ProductModel
        fields = '__all__'
        read_only_fields = 'status_display', 'user_owner_display', 'images', 'order', 'price_display', 'category_display'
     
        
class PhotoProductSerializer(ModelSerializer):
    class Meta:
        model = PhotoProductModel
        fields = '__all__'