from django.db import models
from django.conf import settings
from products.models import Product, ProductVariant


 
# CART & CART ITEMS
class Cart(models.Model):
    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.customer:
            return f"Cart for {self.customer.username}"
        elif self.session_key:
            return f"Anonymous Cart {self.session_key[:8]}..."
        return f"Cart {self.id}"

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def clear(self):
        self.items.all().delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")

    # Either product OR product_variant must be set
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_cart_product",
                condition=models.Q(product__isnull=False, product_variant__isnull=True),
            ),
            models.UniqueConstraint(
                fields=["cart", "product_variant"],
                name="unique_cart_variant",
                condition=models.Q(product_variant__isnull=False, product__isnull=True),
            ),
        ]

    def __str__(self):
        target = self.product_variant or self.product
        return f"{self.quantity} x {target} in {self.cart}"

    def get_unit_price(self):
        """Return unit price with discounts."""
        target = self.product_variant.product if self.product_variant else self.product
        return target.get_discounted_price()

    def get_subtotal(self):
        return self.get_unit_price() * self.quantity


 
# ORDER & ORDER ITEMS
class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("returned", "Returned"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    destination = models.TextField()
    telephone = models.CharField(max_length=20, blank=True)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="unconfirmed"
    )

    def __str__(self):
        return f"Order {self.id} - {self.customer.username}"

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    # Either product OR product_variant must be set
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # locked-in at checkout
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        target = self.product_variant or self.product
        return f"{self.order} - {target}"

    def get_subtotal(self):
        return (self.unit_price - self.discount) * self.quantity


 
# SAVED ITEMS (Wishlist)
class SavedItem(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_items")

    # Either product OR product_variant must be set
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "product"],
                name="unique_saved_product",
                condition=models.Q(product__isnull=False, product_variant__isnull=True),
            ),
            models.UniqueConstraint(
                fields=["customer", "product_variant"],
                name="unique_saved_variant",
                condition=models.Q(product_variant__isnull=False, product__isnull=True),
            ),
        ]

    def __str__(self):
        target = self.product_variant or self.product
        return f"{self.customer.username} saved {target}"
