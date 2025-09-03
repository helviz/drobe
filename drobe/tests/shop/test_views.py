from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
import pytest, json, faker
from django.test import RequestFactory
from shop.views import updateitem, processOrder

pytestmark = pytest.mark.django_db
fake = faker.Faker()

def test_index(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/index.html")
    
def test_shop(client):
    response = client.get(reverse('shop'))
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/shop.html")
    
def test_cart(client):
    response = client.get(reverse('cart'))
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/cart.html")
    
def test_checkout(client):
    response = client.get(reverse('checkout'))
    assert response.status_code == 302
    if response.status_code == 200:
        assertTemplateUsed(response, "shop/checkout.html")
    
def test_update_item(client, user_factory, product_factory, order_factory):
    user = user_factory()
    product = product_factory()
    order = order_factory(customer=user)
    data = {'productId': product.id, 'action': 'add'}
    request = RequestFactory().post('/updateitem/', data=json.dumps(data), content_type='application/json')
    request.user = user
    response = updateitem(request)
    assert response.status_code == 200
    
    
def test_process_order(client, user_factory, product_factory, order_factory):
    user = user_factory()
    product = product_factory()
    order = order_factory(customer=user)
    data = {'form': {'first_name':'mulindwa','last_name':'sulaiman','email':fake.email(), 'total':10000}}
    request = RequestFactory().post('/process-order/', data=json.dumps(data), content_type='application/json')
    request.user = user
    response = processOrder(request)
    assert response.status_code == 200
    
def test_view_product(client):
    response = client.get(reverse('view-product', args=[1]))
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/product.html")
    
def test_about(client):
    response = client.get(reverse('about'))
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/about.html")

def test_category(client):
    response = client.get(reverse("category", args=['misc']))
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/shop.html")