from .models import Cart

def cart_count(request):
    cart_items_count = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(customer=request.user).first()
        if cart:
            cart_items_count = sum(item.quantity for item in cart.items.all())

    else:
        # Ensure session exists
        if not request.session.session_key:
            request.session.create()

        cart = Cart.objects.filter(session_key=request.session.session_key, customer__isnull=True).first()
        if cart:
            cart_items_count = sum(item.quantity for item in cart.items.all())

    return {'cart_items_count': cart_items_count}
