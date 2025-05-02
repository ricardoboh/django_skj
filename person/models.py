from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    birthdays = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    newsletters = models.BooleanField(default=False)

    def __str__(self):
        return f"Customer {self.name} {self.surname}"

class DeliveryGuy(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    hire_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Delivery Guy {self.name} {self.surname}"
