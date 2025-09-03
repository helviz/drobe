import factory, faker
from django.contrib.auth.models import User
from shop.models import *
from authentication.models import *

fake = faker.Faker()

#authentication factories
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        
    username = factory.Faker('user_name')  # Generating a fake username
    password = factory.Faker('password')   # Generating a fake password
    is_superuser = True                    # Setting user as superuser
    is_staff = True                        # Setting user as staff

class BusinessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Business
        
    owner = factory.SubFactory(UserFactory)    # Creating a user as the owner
    first_name = factory.Faker('first_name')   # Generating a fake first name
    last_name = factory.Faker('last_name')     # Generating a fake last name
    business_name = factory.Faker('company')   # Generating a fake business name
    email = fake.email()                       # Generating a fake email address

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        
    user = factory.SubFactory(UserFactory)   # Creating a user profile
    image = fake.image_url()                 # Generating a fake image URL
    
class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer
        
    user = factory.SubFactory(UserFactory)   # Creating a user as a customer
    first_name = fake.first_name()           # Generating a fake first name
    last_name = fake.last_name()             # Generating a fake last name
    email = fake.email()                      # Generating a fake email address
    
# Shop factories
    
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        
    category_name = factory.Faker("word")    # Generating a fake category name
    
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        
    name = factory.Faker('word')             # Generating a fake product name
    description = factory.Faker('text')       # Generating a fake description
    owner = factory.SubFactory(BusinessFactory)  # Creating a business as the owner
    price = f"{fake.random_int()}"           # Generating a random price
    digital = factory.Faker('boolean')       # Generating a boolean for digital
    image = factory.Faker('image_url')       # Generating a fake image URL
    category = factory.SubFactory(CategoryFactory)  # Creating a category for the product
    
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
    
    customer = factory.SubFactory(UserFactory)   # Creating a user as the customer
    complete = fake.boolean()                   # Generating a boolean for completion
    transaction_id = fake.random_number()       # Generating a random transaction ID
    
class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem
    
    product = factory.SubFactory(ProductFactory)  # Creating a product for the order item
    order = factory.SubFactory(OrderFactory)      # Creating an order for the order item
    quantity = 0                                  # Setting quantity to 0 initially

class ShippingAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShippingAddress
    
    customer = factory.SubFactory(UserFactory)    # Creating a user as the customer
    order = factory.SubFactory(OrderFactory)      # Creating an order for the shipping address
    address = fake.address()                      # Generating a fake address
    city = fake.city()                            # Generating a fake city
    state = fake.state()                          # Generating a fake state
    zipcode = fake.zipcode()                      # Generating a fake ZIP code

