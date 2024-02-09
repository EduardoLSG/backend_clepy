from django.shortcuts import render
from .models import CategoryModel, ProductModel, PhotoProductModel
from rest_framework.viewsets import ModelViewSet
from system.views import DefaultAPIView
from .serializers import CategorySerializer, ProductSerializer, PhotoProductSerializer


class CategoryViewset(ModelViewSet, DefaultAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    

class ProductViewset(ModelViewSet, DefaultAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    
class PhotoProductViewSet(ModelViewSet, DefaultAPIView):
    queryset = PhotoProductModel.objects.all()
    serializer_class = PhotoProductSerializer