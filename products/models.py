from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid
from taggit.managers import TaggableManager


# IMAGE PATH HELPERS
def brand_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return f"brands/{filename}"

def product_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return f"products/{filename}"

def variant_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return f"products/variants/{filename}"


# CATEGORY
class Category(models.TextChoices):
    MENS_CLOTHING = 'MENS', "Men's Clothing"
    WOMENS_CLOTHING = 'WOMENS', "Women's Clothing"
    KIDS_CLOTHING = 'KIDS', "Kids' Clothing"
    SHOES = 'SHOES', "Shoes"
    ACCESSORIES = 'ACCESSORIES', "Accessories"
    ACTIVEWEAR = 'ACTIVEWEAR', "Activewear"
    OUTERWEAR = 'OUTERWEAR', "Outerwear"


# BRAND
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to=brand_image_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# PRODUCT
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.MENS_CLOTHING)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    tags = TaggableManager()
    image = models.ImageField(upload_to=product_image_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"

    def get_active_discounts(self):
        """Return all currently active discounts applicable to this product."""
        now = timezone.now()
        discounts = self.discounts.filter(active=True, start_date__lte=now).exclude(end_date__lt=now)
        # Include brand discounts
        for brand_discount in self.brand.discounts.filter(active=True, start_date__lte=now).exclude(end_date__lt=now):
            discounts |= Discount.objects.filter(pk=brand_discount.pk)
        # Include category discounts
        for discount in Discount.objects.filter(active=True, start_date__lte=now):
            if self.category in discount.categories:
                discounts |= Discount.objects.filter(pk=discount.pk)
        return discounts.distinct()

    def get_discounted_price(self):
        price = self.price
        discounts = self.get_active_discounts()
        for discount in discounts:
            if discount.discount_type == Discount.PERCENTAGE:
                price -= (price * discount.value / Decimal('100.0'))
            elif discount.discount_type == Discount.FIXED:
                price -= discount.value
        return max(price, Decimal('0.0'))


# PRODUCT VARIANT
class ProductVariant(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'),
        ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', '2XL'),
    ]
    COLOR_CHOICES = [
        ('RED', 'Red'), ('BLUE', 'Blue'), ('GREEN', 'Green'), ('BLACK', 'Black'),
        ('WHITE', 'White'), ('YELLOW', 'Yellow'), ('ORANGE', 'Orange'), ('PINK', 'Pink'),
        ('PURPLE', 'Purple'), ('BROWN', 'Brown'), ('GREY', 'Grey'), ('BEIGE', 'Beige'),
        ('NAVY', 'Navy'), ('MAROON', 'Maroon'), ('OLIVE', 'Olive'), ('TEAL', 'Teal'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)

    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to=variant_image_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'size', 'color')

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.color}"


# DISCOUNT
class Discount(models.Model):
    # Discount types
    PERCENTAGE = 'PERCENTAGE'
    FIXED = 'FIXED'
    DISCOUNT_TYPE_CHOICES = [
        (PERCENTAGE, 'Percentage'),
        (FIXED, 'Fixed Amount'),
    ]

    # Priority for conflict resolution
    PRIORITY_PRODUCT = 'PRODUCT'
    PRIORITY_BRAND = 'BRAND'
    PRIORITY_CATEGORY = 'CATEGORY'
    PRIORITY_CHOICES = [
        (PRIORITY_PRODUCT, 'Product'),
        (PRIORITY_BRAND, 'Brand'),
        (PRIORITY_CATEGORY, 'Category'),
    ]

    # Core fields
    name = models.CharField(max_length=100)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    value = models.DecimalField(
        max_digits=8, decimal_places=2, help_text="Percentage or fixed amount"
    )
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_PRODUCT,
        help_text="Priority when multiple discounts apply"
    )

    # Relations
    products = models.ManyToManyField(Product, blank=True, related_name='discounts')
    brands = models.ManyToManyField(Brand, blank=True, related_name='discounts')
    categories = models.JSONField(
        blank=True, default=list,
        help_text="List of categories (use Category enum values)"
    )

    class Meta:
        ordering = ['-priority', 'name']

    def is_active(self):
        """Check if discount is currently active based on dates and active flag."""
        today = timezone.now().date()  # convert to date
        return (
            self.active
            and (self.start_date <= today)
            and (not self.end_date or today <= self.end_date)
        )

    def applies_to_product(self, product: Product) -> bool:
        """Check if this discount applies to the given product."""
        if not self.is_active():
            return False
        if self.products.filter(pk=product.pk).exists():
            return True
        if self.brands.filter(pk=product.brand.pk).exists():
            return True
        if product.category in self.categories:
            return True
        return False

    def __str__(self):
        return f"{self.name} ({self.discount_type} - {self.value})"



# PRODUCT REVIEW
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=5)  # 1–5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    class Meta:
        unique_together = ('product', 'user', 'variant')

    def __str__(self):
        variant_info = f" - {self.variant.size}/{self.variant.color}" if self.variant else ""
        return f"{self.user.username} - {self.product.name}{variant_info} ({self.rating}⭐)"
