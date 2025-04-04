Update from: 2025-03-10/11:37
# django_skj
Project in Django framework for the VSB subject Script languages in Python.

# Apps
- order
- person
- delivery
- management
- restaurant
- product
- eshop

# Models
- Person
-   Customer
-   DeliveryGuy
- Order
- Payment
- Product
- Restaurant
- OrderProduct
- DeliveryStatus
- Review

# Initialization of environment
1. Python virtual env
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Django install
```bash
pip install django djangorestframework django-environ

pip freeze > requirements.txt
python manage.py migrate
python manage.py runserver
```






