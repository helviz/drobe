from django.urls import resolve
from shop.views import *

class TestUrls:
        def test_home_url(self):
            url = resolve('/')
            assert url.func == index
            assert url.view_name == 'home'

        def test_shop_url(self):
            url = resolve('/shop/')
            assert url.view_name == 'shop'
            

        def test_cart_url(self):
            url = resolve('/cart/')
            assert url.view_name == 'cart'
            assert url.func == cart

        def test_checkout_url(self):
            url = resolve('/checkout/')
            assert url.view_name == 'checkout'
            assert url.func == checkout

        def test_update_item_url(self):
            url = resolve('/update-item/')
            assert url.view_name == 'update-item'
            assert url.func == updateitem

        def test_process_order_url(self):
            url = resolve('/process-order/')
            assert url.view_name == 'process-order'
            assert url.func == processOrder

        def test_view_product_url(self):
            url = resolve('/product-view/4/')
            assert url.view_name == 'view-product'
            assert url.func == viewProduct
            
        def test_about_url(self):
            url = resolve('/about/')
            assert url.view_name == 'about'
            assert url.func == about
            
        def test_category_url(self):
            url = resolve('/category/misc/')
            assert url.view_name == 'category'
            assert url.func == category
