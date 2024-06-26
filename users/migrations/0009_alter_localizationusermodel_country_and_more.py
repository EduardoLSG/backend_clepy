# Generated by Django 5.0.1 on 2024-04-13 23:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_alter_usermodel_photo_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="localizationusermodel",
            name="country",
            field=models.CharField(
                default="BRASIL", max_length=50, verbose_name="Pais"
            ),
        ),
        migrations.AlterField(
            model_name="localizationusermodel",
            name="district",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Bairro"
            ),
        ),
        migrations.AlterField(
            model_name="localizationusermodel",
            name="number",
            field=models.IntegerField(blank=True, null=True, verbose_name="Numero"),
        ),
        migrations.AlterField(
            model_name="localizationusermodel",
            name="street",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Endereço"
            ),
        ),
    ]
