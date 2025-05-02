from django.urls import path
from . import views

urlpatterns = [
    # Form for the employee
    path('form/', views.call_center_order_form, name='call_center_form'),

    # Endpoints for the form
    path('delivery-guys/', views.get_active_delivery_guys, name='get_active_delivery_guys'),
    path('search-restaurants/', views.search_restaurants, name='search_restaurants'),
    path('menu-products/', views.get_menu_by_restaurant, name='get_menu_by_restaurant'),
    path('finish-order/', views.finish_order, name='finish_order'),
    path('cancel-order/', views.cancel_order, name='cancel_order'),

    # Endpoints for the buttons in active orders
    path("<int:order_id>/verify-toggle/", views.verify_toggle, name="order_verify_toggle"),
    path("<int:order_id>/cancel/", views.cancel_active_order, name="order_cancel"),
    path("<int:order_id>/print/", views.print_order, name="order_print"),

    # Ending the shift endpoint
    path('shift-end/', views.end_shift, name='end_shift'),
]