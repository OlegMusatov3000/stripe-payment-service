from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Item(models.Model):
    name = models.CharField('Имя', max_length=255)
    description = CKEditor5Field(
        verbose_name='Описание', max_length=600,
        config_name='extends', default='Описание'
    )
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    items = models.ManyToManyField(
        Item, related_name='orders', verbose_name='Товары',
    )
    payment_intent_id = models.CharField(
        'Идентификатор платежного интента в системе Stripe',
        max_length=255, blank=True, null=True
    )

    def calculate_total_price(self):
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return f"Order {self.id}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
