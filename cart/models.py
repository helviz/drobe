from django.db import models
from django.conf import settings
from products.models import ProductVariant

class Order(models.Model):
    STATUS_CHOICES = [
        ("unconfirmed", "Unconfirmed"),
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("returned", "Returned"),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    destination = models.TextField()
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unconfirmed")

    def __str__(self):
        return f"Order {self.id} - {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order} - {self.product_variant}"


class SavedItem(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_items")
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.username} saved {self.product_variant}"

