from django.db import models
from authentication.models import Business
from django.contrib.auth.models import User
import os, uuid


# Function to rename uploaded image files
def rename_image(instance, form_picture):
    _, f_ext = os.path.splitext(form_picture)
    new_file_name = "%s%s" % (uuid.uuid4(), f_ext)
    return new_file_name

# Model representing categories of products
class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return f"{self.category_name}"

# Model representing products
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)  # Link to Business model
    price = models.DecimalField(max_digits=12, decimal_places=2)
    digital = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, max_length=500)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    rating = models.DecimalField(default=0.0, decimal_places=1, max_digits=3)

    def __str__(self):
        return f"{self.name} costs {self.price}"

    # Property to get the URL of the product's image
    @property
    def imageurl(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    # Override save method to rename image file
    def save(self, *args, **kwargs):
        if not self.id:
            self.image.name = rename_image(self, self.image.name)
        super().save(*args, **kwargs)

# Model representing orders
class Order(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True  # Link to User model
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}"

    # Property to get the total cost of items in the cart
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_items_in_cart(self):
        orderitems = self.orderitem_set.all()
        return orderitems

    # Property to check if shipping is required for the order
    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()
        for item in orderItems:
            if item.product.digital == False:
                shipping = True
        return shipping

    # Property to get the total number of items in the cart
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

# Model representing items in an order
class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True  # Link to Product model
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)  # Link to Order model
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}".format(self.product.name)

    # Property to get the total cost of the order item
    @property
    def get_total(self):
        total = 0
        if self.product:
            total = self.product.price * self.quantity
        return total

# Model representing shipping addresses for orders
class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True  # Link to User model
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)  # Link to Order model
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=50, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
