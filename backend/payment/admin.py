from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Item, Order

admin.site.unregister(Group)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('id', 'name', 'price')
    list_display_links
    list_filter = ('name',)
    search_fields = ('description', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('payment_intent_id',)
    list_filter = ('items__name',)
    search_fields = ('payment_intent_id',)
    filter_horizontal = ('items',)
