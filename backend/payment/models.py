from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Item(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'Доллары'),
        ('RUB', 'Рубли'),
    ]

    name = models.CharField('Имя', max_length=255)
    description = CKEditor5Field(
        verbose_name='Описание', max_length=600,
        config_name='extends', default='Описание'
    )
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    currency = models.CharField(
        'Валюта', max_length=3, choices=CURRENCY_CHOICES, default='RUB'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Discount(models.Model):
    name = models.CharField('Название', max_length=255)
    amount = models.DecimalField(
        '% скидки', max_digits=10, decimal_places=2
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Tax(models.Model):
    name = models.CharField('Название', max_length=255)
    rate = models.DecimalField('Ставка налога', max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'


class Order(models.Model):
    items = models.ManyToManyField(
        Item, related_name='orders', verbose_name='Товары',
    )
    payment_intent_id = models.CharField(
        'Идентификатор платежного интента в системе Stripe',
        max_length=255, blank=True, null=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Пользователь, который совершает покупку'
    )
    total_price = models.FloatField(
        'Стоимость заказа', blank=True, null=True
    )
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL,
        blank=True, null=True, verbose_name='Скидка'
    )
    tax = models.ForeignKey(
        Tax, on_delete=models.SET_NULL, blank=True,
        null=True, verbose_name='Налог'
    )

    def calculate_total_price(self):
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return f"Order {self.id}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
