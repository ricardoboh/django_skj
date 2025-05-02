"""
URL configuration for eshop_skj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Admin
    path('admin/', admin.site.urls),

    # Notebook
    path('active/', views.active_tab, name='active_orders'),
    path('history/', views.history_tab, name='history_orders'),
    path('end_of_shift/', views.end_shift_tab, name='end_of_shift'),

    # Orders pages
    path('call-center-form/', views.form_handle, name='form'),
    path('products/', views.customer_menu, name='main_product_page'),
    path('customer_place_order/', views.customer_place_order, name='order_placement'),

    # User management
    path('person/', include('person.urls')),

    # Orders management
    path('order/', include('order.urls')),

    # Restaurant management
    # path('restaurant/', include('restaurant.urls')),
]
