from django.db import models

from products.models import ProductSize


class ProductReservation(models.Model):
    product_size = models.ForeignKey(
        ProductSize, on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    session_key = models.CharField(max_length=32)
    reversed_at = models.DateTimeField(auto_now_add=True)
