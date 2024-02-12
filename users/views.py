from .models import *
from rest_framework.viewsets import ModelViewSet
from .serializers import  *
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from system.views import DefaultAPIView
from rest_framework.response import Response
from rest_framework import status as resp_status
from django.contrib.auth import authenticate


class UserCreateAPIView(CreateAPIView):
    queryset = UserModel
    serializer_class = UserCreateSerializer


class LoginAPIView(APIView):
    def post(self, request, format=None):
        data = request.data

        email = data.get('email', None)
        password = data.get('password', None)
        print(email, password)
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                token = Token.objects.get(user=user)
                return Response({'token': token.key}, status=resp_status.HTTP_200_OK)
            else:
                return Response(status=resp_status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=resp_status.HTTP_404_NOT_FOUND)


class UserViewSet(DefaultAPIView, ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class  = UserSerializer
    http_method_names = ['get', 'patch', 'delete']
    
    def validate_user(self, user, user_pk):
        if not user.is_superuser and user_pk != user.pk:
            return False, Response({'msg': 'User sem permissão'}, status=resp_status.HTTP_401_UNAUTHORIZED)

        return True, 'Ok'
      
    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk            
        return super().create(request, *args, **kwargs)
    
    
    def list(self, request, *args, **kwargs):
        user = request.user
        
        if not user.is_superuser:
            return Response({'msg': 'User sem permissão'}, status=resp_status.HTTP_401_UNAUTHORIZED)
           
        return super().list(request, *args, **kwargs)
    
    
    def retrieve(self, request, *args, **kwargs):
        
        user = request.user
        id_user = kwargs.get('pk')
        
        valid_user, resp = self.validate_user(user, id_user)
        if not valid_user:
            return resp
        
        return super().retrieve(request, *args, **kwargs)
    

    def update(self, request, *args, **kwargs):
        
        user = request.user
        id_user = kwargs.get('pk')
        
        valid_user, resp = self.validate_user(user, id_user)
        if not valid_user:
            return resp
        
        return super().update(request, *args, **kwargs)


    def destroy(self, request, *args, **kwargs):
        
        user = request.user
        id_user = kwargs.get('pk')
        
        valid_user, resp = self.validate_user(user, id_user)
        if not valid_user:
            return resp
        
        return super().destroy(request, *args, **kwargs)


class LocalizationUserViewSet(DefaultAPIView, ModelViewSet):
    queryset = LocalizationUserModel.objects.all()
    serializer_class = LocalizationUserSerializer
    
    
    def validate_localization(self, pk, user):
        if not LocalizationUserModel.objects.filter(user=user, pk=pk).exists():
            return False, Response({'msg': 'User sem permissão'}, status=resp_status.HTTP_401_UNAUTHORIZED)
        
        return True, 'Ok'
    
    
    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk            
        return super().create(request, *args, **kwargs)
       
    
    def retrieve(self, request, *args, **kwargs):
        
        user = request.user      
        pk_loc = kwargs.get('pk')
        
        valid_loc, resp = self.validate_localization(pk_loc, user)
        if not valid_loc:
            return resp        
        
        return super().retrieve(request, *args, **kwargs)
    

    def update(self, request, *args, **kwargs):
        
        user = request.user
        pk_loc = kwargs.get('pk')
        
        valid_loc, resp = self.validate_localization(pk_loc, user)
        if not valid_loc:
            return resp  
        
        return super().update(request, *args, **kwargs)


    def destroy(self, request, *args, **kwargs):
        
        user = request.user
        pk_loc = kwargs.get('pk')
        
        valid_loc, resp = self.validate_localization(pk_loc, user)
        if not valid_loc:
            return resp
        
        return super().destroy(request, *args, **kwargs)

    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

