from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import CategoryModel, ProductModel, PhotoProductModel


class CategorySerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'
        

class ProductSerializer(ModelSerializer):
    
    images = serializers.SerializerMethodField('get_images')
    
    def get_images(self, obj):
        photos = PhotoProductModel.objects.filter(product=obj.pk).order_by('order')
        data = []
        for photo in photos:
            data.append({'url': photo.photo.url, 'id': str(photo.id)})
        return data
    
    class Meta:
        model = ProductModel
        fields = '__all__'
     
        
class PhotoProductSerializer(ModelSerializer):
    class Meta:
        model = PhotoProductModel
        fields = '__all__'