from django.contrib import admin
from .models import Category, Product, ProductVariant, ProductReview, DiscountItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "price", "stock_quantity", "is_primary")
    list_filter = ("is_primary", "product__category")
    search_fields = ("product__name",)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "product_variant", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("customer__username", "product_variant__product__name")


@admin.register(DiscountItem)
class DiscountItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product_variant", "date_from", "date_to", "amount_discounted")
    list_filter = ("date_from", "date_to")
    search_fields = ("product_variant__product__name",)

