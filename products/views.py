from django.shortcuts import render
from .models import CategoryModel
# Create your views here.


list_category = [ 'Informática',
    'Som e Iluminação',
    'Música',
    'Brinquedos para festa',
    'Eletrodoméstico',
    'Construção',
    'Equipamentos fotográficos',
    'Festas',
    'Games',
    'Fitness',
    'Equipamentos hospitalares',
    'Outros']


# for cat in list_category:
#     CategoryModel.objects.create(
#         name = cat
#     )
