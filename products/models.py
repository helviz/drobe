from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.price}"


class ProductReview(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="reviews")
    comment = models.TextField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.product_variant.product.name}"


class DiscountItem(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="discounts")
    date_from = models.DateField()
    date_to = models.DateField()
    amount_discounted = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Discount on {self.product_variant} ({self.amount_discounted})"
