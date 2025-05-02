from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from order.models import Shift, Order, Restaurant, MenuProduct, OrderMenu
from person.models import DeliveryGuy, Customer
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.urls import reverse
from django.utils import timezone
from order.views import get_current_shift


# Order states
DRAFT_STATE = 'Neověřeno'
PLACED_STATE = 'Ověřeno'
CANCELLED_STATE = 'Storno'


# Home page for all users
def home(request):
    if request.user.is_staff:
        # staff sees the delivery‐guy dashboard
        return redirect('active_orders')
    elif request.user.is_authenticated:
        # normal customer homepage
        return redirect('main_product_page')
    else:
        return redirect('login')
    

# Notebook tab for active orders
@login_required
def active_tab(request):
    current_shift = (Shift.objects
                     .filter(end__isnull=True)
                     .first())
    
    orders = (Order.objects
              .filter(shift=current_shift, state__in=[DRAFT_STATE, PLACED_STATE])
              .order_by('order_date'))

    return render(request, 'active_orders.html', {'orders': orders, 'active_tab': 'active_orders',})

# Notebook tab for history orders
@login_required
def history_tab(request):
    current = (Shift.objects
               .filter(end__isnull=True)
               .first())
    
    orders = (Order.objects
              .filter(shift=current)
              .order_by('-order_date'))

    delivery_guys = DeliveryGuy.objects.filter(active=True)

    return render(request, 'history_orders.html', {
        'orders': orders,
        'delivery_guys': delivery_guys,
        'active_tab': 'history_orders',
    })

# Notebook tab for shift end form
@login_required
def end_shift_tab(request):
    return render(request, 'shift_end.html', { 'active_tab': 'end_of_shift',})

# Order form
def form_handle(request):
    return render(request, 'form.html')

# Product page
def customer_menu(request):
    restaurants = (Restaurant.objects
                   .filter(open=True))
    return render(request, 'menu.html', {'restaurants': restaurants})

# Doing the Order from the Customer view
@require_POST
def customer_place_order(request):
    try:
        data = json.loads(request.body)

        customer = Customer.objects.get(pk=data['customer_id'])
        restaurant = Restaurant.objects.get(pk=data['restaurant_id'])
        shift = get_current_shift()

        order = Order.objects.create(
            shift = shift,
            customer = customer,
            restaurant = restaurant,
            state = DRAFT_STATE,
        )

        total = 0.0
        for line in data.get('lines', []):
            menu_product_api = MenuProduct.objects.get(pk=line['menu_product_id'])
            quantity_api = int(line['quantity'])
            part = menu_product_api.price * quantity_api
            OrderMenu.objects.create(
                order=order,
                menu_product=menu_product_api,
                quantity=quantity_api,
                price_part=part
            )
            total += part

        order.price_total = total
        order.save()

        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'redirect_url': reverse('main_product_page')
        })

    except Restaurant.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid restaurant'}, status=400)
    except MenuProduct.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid menu item'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
