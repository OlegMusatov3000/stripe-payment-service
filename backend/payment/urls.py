from django.urls import path
from .views import buy_item, item_detail, success_page, cancel_page

urlpatterns = [
    path('buy/<int:item_id>/', buy_item, name='buy_item'),
    path('item/<int:item_id>/', item_detail, name='item_detail'),
    path('success/', success_page, name='success_page'),
    path('cancel/', cancel_page, name='cancel_page'),
]
