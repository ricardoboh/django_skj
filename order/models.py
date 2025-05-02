from django.db import models
from person.models import Customer, DeliveryGuy
from restaurant.models import Restaurant, MenuProduct
from django.utils import timezone

class Shift(models.Model):
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.end:
            return f"Shift {self.start:%Y-%m-%d %H:%M} - {self.end:%H:%M}"
        return f"Shift {self.start:%Y-%m-%d %H:%M} is stil open."

class Order(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    delivery_guy = models.ForeignKey(DeliveryGuy, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=30)
    price_total = models.FloatField(null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order No.{self.id} - {self.customer.name}"

class OrderMenu(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_product = models.ForeignKey(MenuProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_part = models.FloatField()

    def __str__(self):
        return f"{self.quantity}x {self.menu_product.name}"

