from django.contrib import admin
from .models import Order, OrderItem, SavedItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # show 1 empty row for adding new items
    autocomplete_fields = ["product_variant"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "paid", "date")
    list_filter = ("status", "paid", "date")
    search_fields = ("customer__username", "destination")
    inlines = [OrderItemInline]


@admin.register(SavedItem)
class SavedItemAdmin(admin.ModelAdmin):
    list_display = ("customer", "product_variant")
    search_fields = ("customer__username", "product_variant__product__name")


# If you also want OrderItem visible separately in admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_variant", "quantity", "discount")
    search_fields = ("order__id", "product_variant__product__name")
