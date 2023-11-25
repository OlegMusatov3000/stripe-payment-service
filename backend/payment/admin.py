from django.contrib import admin
from django.contrib.auth.models import Group
from django.http.request import HttpRequest

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
    list_display = list_display_links = (
        'payment_intent_id', 'total_price', 'user'
    )
    list_filter = ('items__name', 'user__username')
    search_fields = ('payment_intent_id',)
    readonly_fields = ('items', 'payment_intent_id', 'user', 'total_price')

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
