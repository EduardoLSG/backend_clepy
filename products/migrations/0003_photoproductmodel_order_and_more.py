# Generated by Django 5.0.1 on 2024-02-14 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_categorymodel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='photoproductmodel',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='photoproductmodel',
            unique_together={('product', 'order')},
        ),
    ]
