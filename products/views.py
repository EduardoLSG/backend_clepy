from django.shortcuts import render
from .models import CategoryModel, ProductModel, PhotoProductModel
from rest_framework.viewsets import ModelViewSet
from system.views import DefaultAPIView
from .serializers import CategorySerializer, ProductSerializer, PhotoProductSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status as resp_status

class CategoryViewset(ModelViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get']  

class ProductViewset(ModelViewSet, DefaultAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    
    def validate_product_user(self, user, product_pk):
        if not ProductModel.objects.filter(user_id=user, id=product_pk).exists():
            return False, Response({'msg': 'User sem permissão'}, status=resp_status.HTTP_401_UNAUTHORIZED)

        return True, 'Ok'
      
    def create(self, request, *args, **kwargs):
        user = request.user
        user_owner = request.data['user_owner']
        
        if str(user.pk) != str(user_owner):
            return  Response({'msg': 'User sem permissão'}, status=resp_status.HTTP_401_UNAUTHORIZED)
               
        return super().create(request, *args, **kwargs) 
    
    def list(self, request, *args, **kwargs):           
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):        
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        
        user       = request.user
        id_product = kwargs.get('pk')
        
        valid_user, resp = self.validate_product_user(user, id_product)
        if not valid_user:
            return resp
        
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        
        user    = request.user
        id_product = kwargs.get('pk')
        
        valid_user, resp = self.validate_product_user(user, id_product)
        if not valid_user:
            return resp
        
        return super().destroy(request, *args, **kwargs)

class ProductListAPIView(ListAPIView, RetrieveAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    throttle_scope   = 'products'
    
class PhotoProductViewSet(ModelViewSet, DefaultAPIView):
    queryset = PhotoProductModel.objects.all()
    serializer_class = PhotoProductSerializer
    
    def validate_product_user(self, user):
        if not PhotoProductModel.objects.filter(product__user__pk=user.pk).exists():
            return False, Response({'msg': 'User sem permissão'}, status=resp_status.HTTP_401_UNAUTHORIZED)

        return True, 'Ok'
      
    def create(self, request, *args, **kwargs):
        user = request.user
        id_product = request.data['product']
        
        valid_user, resp = self.validate_product_user(user)
        if not valid_user:
            return resp
             
        return super().create(request, *args, **kwargs) 
    
    def list(self, request, *args, **kwargs):           
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):        
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        user       = request.user
        id_product = kwargs.get('pk')
        
        valid_user, resp = self.validate_product_user(user)
        if not valid_user:
            return resp
        
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):      
        user    = request.user
        id_product = kwargs.get('pk')
        
        valid_user, resp = self.validate_product_user(user)
        if not valid_user:
            return resp
        
        return super().destroy(request, *args, **kwargs)
 