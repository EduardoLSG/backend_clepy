from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'category-router', CategoryViewset, basename='category-crud')
router.register(r'product-router', ProductViewset, basename='product-crud')
router.register(r'photo-product-router', PhotoProductViewSet, basename='photo-product-crud')
router.register(r'product-open-router', ProductReadOnlyViewset, basename='product-read-only')

urlpatterns = [
]

urlpatterns += router.urls
