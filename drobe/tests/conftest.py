from pytest_factoryboy  import register
from .factories import *

register(UserFactory)
register(BusinessFactory)
register(ProfileFactory)
register(CustomerFactory)
register(ProductFactory)
register(CategoryFactory)
register(OrderFactory)
register(OrderItemFactory)
register(ShippingAddressFactory)