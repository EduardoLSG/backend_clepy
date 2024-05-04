from .models import *
from rest_framework.viewsets import ModelViewSet
from .serializers import  *
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from system.views import DefaultAPIView
from rest_framework.response import Response
from rest_framework import status as resp_status
from django.contrib.auth import authenticate
from django.core import exceptions
from django.db import transaction

class UserCreateAPIView(CreateAPIView):
    queryset = UserModel
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                valid, res = self.validate_user_location(request.data)
                if not valid:
                    return Response(res, status=resp_status.HTTP_400_BAD_REQUEST)
                res = super().create(request, *args, **kwargs)
                loc_user = self.create_location(res)
                res.data['city'] = loc_user.city
                res.data['state'] = loc_user.state
                res.data['postal_code'] = loc_user.postal_code
                return res
        
        except exceptions.ValidationError as e:
            return e
        
        
    
    def validate_user_location(self, data):
        dict_erros = {}
        valid = True
        if 'city' not in data.keys():
            valid = False
            dict_erros['city'] =  ['Este campo é obrigatório']
        
        if 'state' not in data.keys():
            valid = False
            dict_erros['state'] =  ['Este campo é obrigatório']
        
        if 'postal_code' not in data.keys():
            valid = False
            dict_erros['postal_code'] =  ['Este campo é obrigatório']
        
        return valid, dict_erros
            
    def create_location(self, res):
        return LocalizationUserModel.objects.create(
            user_id = res.data['id'],
            city = self.request.data['city'],
            state = self.request.data['state'],
            postal_code = self.request.data['postal_code']
        )

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
                return Response({'token': token.key, 'id': user.pk}, status=resp_status.HTTP_200_OK)
            else:
                return Response(status=resp_status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=resp_status.HTTP_404_NOT_FOUND)

class UserViewSet(DefaultAPIView, ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class  = UserSerializer
    http_method_names = ['get', 'patch', 'delete']
    
    def validate_user(self, user, user_pk):
        if not user.is_superuser and user_pk != str(user.pk):
            return False, Response({'msg': 'User sem permissão'}, status=resp_status.HTTP_401_UNAUTHORIZED)

        return True, 'Ok'
    
    
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

