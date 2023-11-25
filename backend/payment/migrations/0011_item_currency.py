# Generated by Django 4.2.7 on 2023-11-25 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_alter_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='currency',
            field=models.CharField(choices=[('USD', 'Доллары'), ('RUB', 'Рубли')], default='RUB', max_length=3, verbose_name='Валюта'),
        ),
    ]
