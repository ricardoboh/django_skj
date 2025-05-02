from django.urls import path
from . import views

urlpatterns = [
    # Form person searching
    path('search-customer/', views.search_customer_by_phone, name='search_customer'),
    path('get-customer-id/', views.get_customer_id, name='customer_id'),

    # User authentification
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Profile management
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('update-customer/', views.update_customer, name='update_customer'),
]
