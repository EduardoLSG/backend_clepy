# Generated by Django 5.0.1 on 2024-02-04 00:15

import main.helpers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_localizatiionusermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='document',
            field=models.CharField(max_length=17, unique=True, verbose_name='document'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='photo_profile',
            field=models.ImageField(upload_to=main.helpers.photo_profile_directory_path, verbose_name='Photo Profile'),
        ),
    ]
