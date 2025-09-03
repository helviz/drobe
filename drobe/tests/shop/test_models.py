import pytest
import faker

pytestmark = pytest.mark.django_db

class TestProductModel:
    def  test_str_return(self, product_factory):
        product = product_factory(name="pods", price="4342.1")
        assert product.__str__() == "pods costs 4342.1"     
        
    def  test_imageurl_return(self, product_factory):
        image_path = faker.Faker().image_url()
        product = product_factory(image=image_path)
        assert product.imageurl != image_path
        
    def  test_save_method(self, product_factory):      
        product = product_factory(image="image.jpg")
        assert product.image.name != "image.jpg"
        
class TestCategoryModel:
    def test_str_return(self, category_factory):
        category = category_factory(category_name="shoes")
        assert category.__str__() == "shoes"
        
class TestOrderModel:
    def test_str_return(self, order_factory):
        order = order_factory()
        assert order.__str__() == str(order.id)
    
    def test_get_cart_items_return(self, order_factory, order_item_factory):
        order = order_factory()
        order_item_factory(order=order, quantity=2)
        order_item_factory(order=order, quantity=4)
        cart_items_total = 6
        assert order.get_cart_items == cart_items_total
    
    def test_get_cart_total_return(self, order_factory, order_item_factory, product_factory):
        order = order_factory()
        product_one = product_factory(price=10000)
        product_two = product_factory(price=20000)
        order_item_factory(order=order, product=product_one,quantity=2)
        order_item_factory(order=order, product=product_two, quantity=4)
        cart_items_total = 100000
        
        assert order.get_cart_total == cart_items_total
    
    def test_shipping_return(self, order_factory, order_item_factory, product_factory):
        order_one = order_factory()
        order_two = order_factory()
        product_one = product_factory(digital=True)
        product_two = product_factory(digital=False)
        
        order_item_factory(order=order_one, product=product_one, quantity=2)
        order_item_factory(order=order_two, product=product_two, quantity=4)
        
        assert order_one.shipping == False
        assert order_two.shipping == True
        
class TestOrderItem:
    def test_str_return(self, order_item_factory, product_factory):
        product = product_factory(name="shoe")
        order_item = order_item_factory(product=product)
        
        assert order_item.__str__() == str(order_item.product.name)
        
    def test_get_total(self, order_item_factory, product_factory):
        product = product_factory(price=4000)
        order_item = order_item_factory(product=product, quantity=5)
        
        assert order_item.get_total == 20000
        
class TestShippingAddress:
    def test_str_return(self, shipping_address_factory):
        shipping_address = shipping_address_factory(address="Kyanja")
        assert shipping_address.__str__() == "Kyanja"
        