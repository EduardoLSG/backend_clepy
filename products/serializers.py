from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import CategoryModel, ProductModel, PhotoProductModel


class CategorySerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'
        

class ProductSerializer(ModelSerializer):
    
    images = serializers.SerializerMethodField('get_images')
    status = serializers.CharField(source='get_status_display')
    user_owner = serializers.SerializerMethodField('get_user_owner')
    
    def get_images(self, obj):
        photos = PhotoProductModel.objects.filter(product=obj.pk).order_by('order')
        data = []
        for photo in photos:
            data.append({'url': photo.photo.url, 'id': str(photo.id)})
        return data    
    
    def get_user_owner(self, obj):
        return {'id': obj.user_owner.id, 'name': obj.user_owner.name}
    
    class Meta:
        model = ProductModel
        fields = '__all__'
     
        
class PhotoProductSerializer(ModelSerializer):
    class Meta:
        model = PhotoProductModel
        fields = '__all__'