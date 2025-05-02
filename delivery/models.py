from django.db import models
from person.models import DeliveryGuy
from order.models import Order

class DeliveryInfo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_guy = models.ForeignKey(DeliveryGuy, on_delete=models.CASCADE)
    state_time = models.DateTimeField()
    state = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.state} for Order #{self.order.id}"
