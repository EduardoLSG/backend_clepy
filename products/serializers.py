from rest_framework.serializers import ModelSerializer
from .models import CategoryModel, ProductModel, PhotoProductModel


class CategorySerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'
        

class ProductSerializer(ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'
     
        
class PhotoProductSerializer(ModelSerializer):
    class Meta:
        model = PhotoProductModel
        fields = '__all__'