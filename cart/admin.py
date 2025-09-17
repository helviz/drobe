from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, SavedItem
  

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("added_at", "get_product_display", "get_price", "get_subtotal")

    def get_product_display(self, obj):
        return obj.product_variant or obj.product

    get_product_display.short_description = "Product / Variant"

    def get_price(self, obj):
        return obj.get_unit_price()

    get_price.short_description = "Unit Price"

    def get_subtotal(self, obj):
        return obj.get_subtotal()

    get_subtotal.short_description = "Subtotal"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "session_key", "created_at", "updated_at", "get_total")
    search_fields = ("customer__username", "session_key")
    inlines = [CartItemInline]

    def get_total(self, obj):
        return obj.get_total()

    get_total.short_description = "Cart Total"


  

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("get_product_display", "unit_price", "discount", "quantity", "get_subtotal")

    def get_product_display(self, obj):
        return obj.product_variant or obj.product

    get_product_display.short_description = "Product / Variant"

    def get_subtotal(self, obj):
        return obj.get_subtotal()

    get_subtotal.short_description = "Subtotal"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "paid", "date", "get_total")
    list_filter = ("status", "paid", "date")
    search_fields = ("customer__username", "id")
    inlines = [OrderItemInline]

    def get_total(self, obj):
        return obj.get_total()

    get_total.short_description = "Order Total"


  

@admin.register(SavedItem)
class SavedItemAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "get_product_display")
    search_fields = ("customer__username",)

    def get_product_display(self, obj):
        return obj.product_variant or obj.product

    get_product_display.short_description = "Product / Variant"
