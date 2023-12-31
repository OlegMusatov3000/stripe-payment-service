# Generated by Django 4.2.7 on 2023-11-24 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='orders', to='payment.item', verbose_name='Товары'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_intent_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Идентификатор платежного интента в системе Stripe'),
        ),
    ]
