# Generated by Django 5.0.1 on 2024-04-30 22:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_photoproductmodel_order_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productmodel",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("0", "WAITING"), ("1", "APPROVED"), ("2", "DISAPPROVED")],
                default="0",
                max_length=2,
                null=True,
                verbose_name="Status",
            ),
        ),
    ]
