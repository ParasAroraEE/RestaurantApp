# Generated by Django 3.1.1 on 2020-09-25 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_auto_20200925_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='bill_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, verbose_name='Total Bill Amount'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='table_number',
            field=models.ForeignKey(default='no table', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='restaurant.tables', verbose_name='Table Number'),
        ),
    ]
