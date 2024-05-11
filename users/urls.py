from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

router = DefaultRouter()

router.register(r'user-router', UserViewSet, basename='user-viewset')
router.register(r'localization-router', LocalizationUserViewSet, basename='localization-viewset')

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name='user-register-api'),
    path("login/", LoginAPIView.as_view(), name='user-login-api'),
    path("social-auth", CustomConvertTokenView.as_view(), name='custom-convert-token-api')
]
urlpatterns += router.urls


