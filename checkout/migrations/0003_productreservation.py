# Generated by Django 3.2.21 on 2023-09-24 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_productsize_options'),
        ('checkout', '0002_order_user_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('session_key', models.CharField(max_length=32)),
                ('reversed_at', models.DateTimeField(auto_now=True)),
                ('product_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productsize')),
            ],
        ),
    ]
