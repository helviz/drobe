from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product, ProductVariant
from decimal import Decimal

User = get_user_model()

class CartViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(name='Test Product', price=Decimal('100.00'))
        self.variant = ProductVariant.objects.create(product=self.product, size='M', color='Red')

    def test_cart_detail_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Shopping Cart')

    def test_cart_detail_anonymous(self):
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_add_product_to_cart(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('add_to_cart'), {
            'product_id': self.product.id,
            'quantity': 2
        })
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.get(customer=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 2)

    def test_add_variant_to_cart(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('add_to_cart'), {
            'product_variant_id': self.variant.id,
            'quantity': 1
        })
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.get(customer=self.user)
        self.assertEqual(cart.items.first().product_variant, self.variant)

    def test_update_cart_item(self):
        self.client.login(username='testuser', password='testpass')
        cart = Cart.objects.create(customer=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        
        response = self.client.post(reverse('update_cart_item'), {
            'cart_item_id': item.id,
            'quantity': 3
        })
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)

    def test_remove_from_cart(self):
        self.client.login(username='testuser', password='testpass')
        cart = Cart.objects.create(customer=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        
        response = self.client.post(reverse('remove_from_cart'), {
            'cart_item_id': item.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CartItem.objects.filter(id=item.id).exists())

    def test_clear_cart(self):
        self.client.login(username='testuser', password='testpass')
        cart = Cart.objects.create(customer=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        
        response = self.client.post(reverse('clear_cart'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(cart.items.count(), 0)

    def test_checkout_requires_login(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)

    def test_checkout_with_items(self):
        self.client.login(username='testuser', password='testpass')
        cart = Cart.objects.create(customer=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Checkout')

    def test_checkout_empty_cart(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)

    def test_process_order(self):
        self.client.login(username='testuser', password='testpass')
        cart = Cart.objects.create(customer=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        response = self.client.post(reverse('process_order'), {
            'telephone': '1234567890',
            'destination': 'Test Address'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(customer=self.user).exists())
        self.assertEqual(cart.items.count(), 0)

    def test_order_list(self):
        self.client.login(username='testuser', password='testpass')
        Order.objects.create(customer=self.user, destination='Test', telephone='123')
        
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Orders')

    def test_anonymous_cart_merge(self):
        # Add item to anonymous cart
        session = self.client.session
        session.create()
        cart = Cart.objects.create(session_key=session.session_key)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        
        # Login and check merge
        self.client.login(username='testuser', password='testpass')
        self.client.get(reverse('cart_detail'))
        
        user_cart = Cart.objects.get(customer=self.user)
        self.assertEqual(user_cart.items.count(), 1)
