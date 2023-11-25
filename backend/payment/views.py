import stripe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from stripe_service_backend.settings import API_KEY
from .models import Item, Order, Discount, Tax


stripe.api_key = API_KEY


@csrf_exempt
@login_required
def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    order = Order.objects.filter(
        user=request.user,
        payment_intent_id=None
    )
    context = {
        'item': item,
        'order': order
    }
    return render(request, 'payment/item_detail.html', context)


@csrf_exempt
@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    order, _ = Order.objects.get_or_create(
        user=request.user,
        payment_intent_id=None,
        discount=Discount.objects.first(),
        tax=Tax.objects.first()
    )
    order.items.add(item)
    return redirect('item_detail', item_id=item_id)


@csrf_exempt
@login_required
def checkout(request, order_id):
    order = get_object_or_404(
        Order, id=order_id, user=request.user, payment_intent_id=None
    )

    item_names = [item.name for item in order.items.all()]
    items_str = ', '.join(item_names)
    unit_amount = int(order.calculate_total_price() * 100)
    discount = order.discount.amount
    tax = order.tax.rate
    currency = order.items.first().currency

    coupon = stripe.Coupon.create(percent_off=discount, duration='once')

    tax_rates = stripe.TaxRate.create(
        display_name="Sales Tax", inclusive=False, percentage=tax
    )

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': currency.lower(),
                'product_data': {
                    'name': f'Покупки: {items_str}',
                },
                'unit_amount': unit_amount,
            },
            'quantity': 1,
            "tax_rates": [tax_rates.id],
        }],
        discounts=[{'coupon': coupon.id}],
        mode='payment',
        success_url=request.build_absolute_uri(reverse(
            'success_page', kwargs={'order_id': order.id}
        )),
        cancel_url=request.build_absolute_uri(reverse(
            'cancel_page', kwargs={'order_id': order.id}
        )),
    )
    order.payment_intent_id = session.id
    order.total_price = session.amount_total / 100
    order.save()
    return JsonResponse({'session_id': session.id})


@csrf_exempt
def success_page(request, order_id):
    order = Order.objects.get(id=order_id)
    template = 'payment/success_page.html'
    context = {
        'total_amount': order.total_price,
        'order_id': order.id
    }
    return render(request, template, context)


@csrf_exempt
def cancel_page(request, order_id):
    order = Order.objects.get(id=order_id)
    template = 'payment/cancel_page.html'
    context = {
        'total_amount': order.total_price,
        'order_id': order.id
    }
    return render(request, template, context)
