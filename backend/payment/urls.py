from django.urls import path
from .views import (
    item_detail, add_to_cart, checkout, success_page, cancel_page
)

urlpatterns = [
    path('item/<int:item_id>/', item_detail, name='item_detail'),
    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('buy/<int:order_id>/', checkout, name='checkout'),
    path('success/<int:order_id>/', success_page, name='success_page'),
    path('cancel/<int:order_id>/', cancel_page, name='cancel_page'),
]
