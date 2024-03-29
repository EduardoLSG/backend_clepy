# Generated by Django 5.0.1 on 2024-02-03 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigAccessModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_var', models.CharField(choices=[('0', 'Pagina'), ('1', 'Endpoint')], default=0, max_length=1, verbose_name='tipo variável')),
                ('var', models.CharField(max_length=255, unique=True, verbose_name='Nome')),
                ('var_name', models.CharField(max_length=25, verbose_name='Nome verificador')),
                ('authorizated', models.BooleanField(default=True, verbose_name='Autorização')),
            ],
        ),
        migrations.CreateModel(
            name='ConfigSysModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='nome váriavel')),
                ('value', models.TextField(verbose_name='valor')),
            ],
            options={
                'verbose_name': 'Variável de sistema',
                'verbose_name_plural': 'Variáveis de sistema',
            },
        ),
    ]
