# Generated by Django 4.2.7 on 2023-11-25 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_alter_discount_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Стоимость заказа'),
        ),
    ]
