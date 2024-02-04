from rest_framework.serializers import ModelSerializer, ValidationError
from .models import UserModel, LocalizationUserModel
import django.contrib.auth.password_validation as validators
from django.core import exceptions


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model  = UserModel
        fields = 'id', 'name', 'email', 'phone', 'document', 'photo_profile', 'password'
        read_only_fields = ('id',)
        
    def validate(self, attrs):
        
        user = UserModel(**attrs)
        
        password = attrs.get('password')
        errors = dict() 
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)
        
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        
        if errors:
            raise ValidationError(errors)
        
        return super().validate(attrs)


    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class UserSerializer(ModelSerializer):
    class Meta:
        model  = UserModel
        exclude = ['password',]
        
    


class LocalizationUserSerializer(ModelSerializer):
    class Meta:
        model  = LocalizationUserModel
        fields = '__all__'