from django.contrib import admin
from django.contrib.auth.models import Group
from django.http.request import HttpRequest

from .models import Item, Order, Tax, Discount

admin.site.unregister(Group)
admin.site.register(Tax)
admin.site.register(Discount)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('id', 'name', 'price', 'currency')
    list_filter = ('name', 'currency')
    search_fields = ('description', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = list_display_links = (
        'payment_intent_id', 'total_price', 'user', 'discount', 'tax'
    )
    list_filter = ('items__name', 'user__username')
    search_fields = ('payment_intent_id',)
    readonly_fields = ('items', 'payment_intent_id', 'user', 'total_price')

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
