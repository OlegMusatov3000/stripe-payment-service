import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse

from stripe_service_backend.settings import API_KEY
from .models import Item, Order


stripe.api_key = API_KEY


@csrf_exempt
def buy_item(request, item_id):
    item = Item.objects.get(pk=item_id)

    order = Order.objects.create()
    order.items.add(item)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f'Order {order.id}',
                },
                'unit_amount': int(order.calculate_total_price() * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success_page')),
        cancel_url=request.build_absolute_uri(reverse('cancel_page')),
    )
    order.payment_intent_id = session.payment_intent
    order.save()

    return JsonResponse({'session_id': session.id})


@csrf_exempt
def item_detail(request, item_id):
    item = Item.objects.get(pk=item_id)
    context = {'item': item}
    template = 'payment/payment.html'
    return render(request, template, context)


def success_page(request):
    template = 'payment/success_page.html'
    return render(request, template)


def cancel_page(request):
    template = 'payment/cancel_page.html'
    return render(request, template)


# @csrf_exempt
# def buy_items(request):
#     item_ids = request.GET.getlist('item_id')

#     if not item_ids:
#         return JsonResponse({'error': 'No item IDs provided'})

#     items = Item.objects.filter(pk__in=item_ids)

#     if not items:
#         return JsonResponse({'error': 'Invalid item IDs'})

#     order = Order.objects.create()

#     for item in items:
#         order.items.add(item)

#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[{
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'name': f'Order {order.id}',
#                 },
#                 'unit_amount': int(order.calculate_total_price() * 100),
#             },
#             'quantity': 1,
#         }],
#         mode='payment',
#         success_url=request.build_absolute_uri(reverse('success_page')),
#         cancel_url=request.build_absolute_uri(reverse('cancel_page')),
#     )
#     order.payment_intent_id = session.payment_intent
#     order.save()

#     return JsonResponse({'session_id': session.id})
