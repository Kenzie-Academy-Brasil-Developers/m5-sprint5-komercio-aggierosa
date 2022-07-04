
from django.db import models

class Product(models.Model):
    descripton = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=8)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    seller = models.ForeignKey("Users.User", on_delete=models.CASCADE, related_name="products")
