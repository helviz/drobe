from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import F
from django.views.decorators.http import require_POST

from .models import Cart, CartItem, OrderItem, Order
from products.models import Product, ProductVariant


  
# Helpers
def _get_or_create_cart(request):
    """Get or create a cart for the current user or session."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(customer=request.user)

        # Merge anonymous cart if it exists
        if request.session.session_key:
            anonymous_cart_qs = Cart.objects.filter(
                session_key=request.session.session_key,
                customer__isnull=True
            )
            if anonymous_cart_qs.exists():
                anonymous_cart = anonymous_cart_qs.first()
                for item in anonymous_cart.items.all():
                    _merge_cart_item(cart, item)
                anonymous_cart.delete()
                request.session.pop('session_key', None)
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key,
            customer__isnull=True
        )
        return cart


def _merge_cart_item(cart, item):
    """Merge a single CartItem into another cart (variant or product)."""
    lookup = {"cart": cart}
    if item.product_variant:
        lookup["product_variant"] = item.product_variant
    else:
        lookup["product"] = item.product

    cart_item, created = CartItem.objects.get_or_create(
        **lookup,
        defaults={"quantity": item.quantity}
    )
    if not created:
        cart_item.quantity += item.quantity
        cart_item.save()


def _get_item_price(item):
    """Return price for a cart item, including variant adjustments and discounts."""
    if item.product_variant:
        base_price = item.product_variant.product.get_discounted_price()
        return base_price + item.product_variant.price_adjustment
    return item.product.get_discounted_price()



def _get_item_name(item):
    """Return display name for a cart item."""
    return str(item.product_variant or item.product)


  
# Views
def cart_detail(request):
    """Displays the contents of the cart."""
    cart = _get_or_create_cart(request)
    cart_items = cart.items.all()
    total_price = sum(_get_item_price(item) * item.quantity for item in cart_items)

    context = {
        "cart": cart,
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, "cart/cart_detail.html", context)


def add_to_cart(request):
    """Adds either a product OR product variant to the cart."""
    if request.method == "POST":
        product_variant_id = request.POST.get("product_variant_id")
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))

        if quantity <= 0:
            messages.error(request, "Quantity must be at least 1.")
            return redirect("cart_detail")

        cart = _get_or_create_cart(request)

        # Determine whether it's a variant or product
        lookup = {"cart": cart}
        if product_variant_id:
            lookup["product_variant"] = get_object_or_404(ProductVariant, id=product_variant_id)
        elif product_id:
            lookup["product"] = get_object_or_404(Product, id=product_id)
        else:
            messages.error(request, "Please select a product or variant.")
            return redirect("cart_detail")

        cart_item, created = CartItem.objects.get_or_create(
            **lookup,
            defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity = F("quantity") + quantity
            cart_item.save()
            cart_item.refresh_from_db()

        messages.success(request, f"{quantity} x {_get_item_name(cart_item)} added to your cart.")
        return redirect("cart_detail")

    return redirect("cart_detail")



def update_cart_item(request):
    """Updates the quantity of a specific cart item."""
    if request.method == "POST":
        cart_item_id = request.POST.get("cart_item_id")
        new_quantity = int(request.POST.get("quantity", 1))

        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart = _get_or_create_cart(request)

        if cart_item.cart != cart:
            messages.error(request, "Invalid cart operation.")
            return redirect("cart_detail")

        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.info(request, f"Quantity for {_get_item_name(cart_item)} updated to {new_quantity}.")
        else:
            messages.warning(request, f"{_get_item_name(cart_item)} removed from your cart.")
            cart_item.delete()

        return redirect("cart_detail")

    return redirect("cart_detail")


def remove_from_cart(request):
    """Removes a specific item from the cart."""
    if request.method == "POST":
        cart_item_id = request.POST.get("cart_item_id")
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart = _get_or_create_cart(request)

        if cart_item.cart != cart:
            messages.error(request, "Invalid cart operation.")
            return redirect("cart_detail")

        messages.warning(request, f"{_get_item_name(cart_item)} removed from your cart.")
        cart_item.delete()
        return redirect("cart_detail")

    return redirect("cart_detail")


def clear_cart(request):
    """Clears all items from the cart."""
    if request.method == "POST":
        cart = _get_or_create_cart(request)
        cart.items.all().delete()
        messages.info(request, "Your cart has been cleared.")
        return redirect("cart_detail")
    return redirect("cart_detail")


@login_required
def checkout(request):
    """Displays the checkout page."""
    cart = _get_or_create_cart(request)
    cart_items = cart.items.all()

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart_detail")

    total_price = sum(_get_item_price(item) * item.quantity for item in cart_items)

    context = {
        "cart": cart,
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, "cart/checkout.html", context)


@require_POST
@login_required
def process_order(request):
    """Handles final order processing."""
    cart = _get_or_create_cart(request)

    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart_detail")

    # ✅ Get telephone & destination from form
    telephone = request.POST.get("telephone", "").strip()
    destination = request.POST.get("destination", "").strip()

    if not telephone or not destination:
        messages.error(request, "Please provide both telephone and destination.")
        return redirect("checkout")  # or wherever your checkout form is

    # 1. Create Order
    order = Order.objects.create(
        customer=request.user,
        telephone=telephone,
        destination=destination,
        paid=False,      # set after integrating payments
        status="pending" # default order status
    )

    # 2. Create OrderItems
    for item in cart.items.all():
        unit_price = item.get_unit_price()
        discount = 0  # TODO: add discount logic later

        OrderItem.objects.create(
            order=order,
            product=item.product if item.product else None,
            product_variant=item.product_variant if item.product_variant else None,
            unit_price=unit_price,
            discount=discount,
            quantity=item.quantity,
        )

    # 3. Clear cart
    cart.clear()

    messages.success(request, "Your order has been placed successfully!")
    return redirect("dashboard")


@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user).order_by("-date")

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("status")
        order = get_object_or_404(Order, id=order_id, customer=request.user)

        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, f"Order {order.id} status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status selected.")

        return redirect("order_list")

    return render(request, "orders/order_list.html", {"orders": orders})

