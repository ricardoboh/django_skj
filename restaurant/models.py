from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} open: {self.open}"

class MenuProduct(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    text_about = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.text_about}"