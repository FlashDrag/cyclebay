# Generated by Django 3.2.21 on 2023-10-01 11:19

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20230930_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(max_length=7, unique=True, validators=[products.models.validate_color]),
        ),
    ]
