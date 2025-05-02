import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone
from person.models import Customer, DeliveryGuy
from restaurant.models import Restaurant, MenuProduct
from .models import Shift, Order, OrderMenu


# Order states
DRAFT_STATE = 'Neověřeno'
PLACED_STATE = 'Ověřeno'
CANCELLED_STATE = 'Storno'


# Form rendering
@login_required
def call_center_order_form(request):
    return render(request, 'form.html')


# The function F6 geting all active deliveries
@require_GET
def get_active_delivery_guys(request):
    deliveries = (DeliveryGuy.objects
                  .filter(active=True)
                  .values('id', 'name', 'surname', 'phone'))
    return JsonResponse(list(deliveries), safe=False)


# The function F8 searching the restaurant by the input fragment
@require_GET
def search_restaurants(request):
    q = request.GET.get('q', '').strip()
    restaurants = (Restaurant.objects
                   .filter(name__icontains=q)
                   .values('id', 'name', 'address', 'phone')[:10])
    return JsonResponse(list(restaurants), safe=False)


# Function F10 geting the products from the restaurant offer
@require_GET
def get_menu_by_restaurant(request):
    try:
        rid = int(request.GET.get('restaurant_id', 0))
    except ValueError:
        return JsonResponse([], safe=False)

    products = MenuProduct.objects.filter(restaurant_id=rid).values(
        'id', 'name', 'price'
    )
    return JsonResponse(list(products), safe=False)


# Finishing order in the Employee view
@require_POST
def finish_order(request):
    try:
        data = json.loads(request.body)

        shift = get_current_shift()
        customer = Customer.objects.get(pk=data['customer_id'])
        dg = (DeliveryGuy.objects.get(pk=data['delivery_guy_id'])
              if data.get('delivery_guy_id') else None)
        restaurant = Restaurant.objects.get(pk=data['restaurant_id'])

        order = Order.objects.create(
            shift=shift,
            customer=customer,
            delivery_guy=dg,
            restaurant=restaurant,
            delivery_address=data.get('delivery_address'),
            state=PLACED_STATE,
        )

        total = 0.0
        for line in data.get('items', []):
            menu_product_api = MenuProduct.objects.get(pk=line['menu_product_id'])
            quantity_api = int(line['quantity'])
            price_line = menu_product_api.price * quantity_api
            OrderMenu.objects.create(
                order=order,
                menu_product=menu_product_api,
                quantity=quantity_api,
                price_part=price_line,
            )
            total += price_line

        order.price_total = total
        order.delivery_date = timezone.now()
        order.save()

        return JsonResponse({'success': True, 'order_id': order.id, 'redirect_url': reverse('active_orders')})

    except Customer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid customer'}, status=400)
    except DeliveryGuy.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid delivery guy'}, status=400)
    except Restaurant.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid restaurant'}, status=400)
    except MenuProduct.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid menu item'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# Canceling order in the employee view
@require_POST
def cancel_order(request):
    return JsonResponse({'success': True, 'redirect_url': reverse('active_orders')})

# Getting the curent shift or starting the new one
def get_current_shift():
    shift = (Shift.objects
             .filter(end__isnull=True)
             .order_by('-start')
             .first())
    
    if not shift:
        shift = Shift.objects.create(start=timezone.now())
    
    return shift

# Ending shift
def end_shift(request):
    shift = (Shift.objects
             .filter(end__isnull=True)
             .first())
    
    if shift:
        shift.end = timezone.now()
        shift.save()
        
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('active_orders'),
        })
    
    return JsonResponse({
        'success': False,
        'error': 'Žádná otevřená směna k uzavření.'
    }, status=400)


# The verifying order if customer created it
@login_required
@require_POST
def verify_toggle(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if order.state == "Neověřeno":
        order.state = "Ověřeno"
    elif order.state == "Ověřeno":
        order.state = "Hotovo"
    else:
        return JsonResponse({"success": False, "error": "Cannot toggle from state "+order.state})
    
    order.save()
    return JsonResponse({"success": True, "new_state": order.state})

# Canceling the order on the employee side in active orders
@login_required
@require_POST
def cancel_active_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.state = "Storno"
    order.save()
    return JsonResponse({"success": True})

# Printing Order in Active tab
@login_required
def print_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "order/print_order.html", {"order": order})