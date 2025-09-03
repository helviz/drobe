from django import forms
from django.contrib.auth.models import User
from authentication.models import Profile,Business,Customer,User
from shop.models import Category, OrderItem, Order, Product, ShippingAddress
class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['first_name', 'last_name', 'business_name', 'email']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'image']

class UserForm(forms.ModelForm):
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")
        
        return password_confirmation
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =['category_name']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields =['product','order','quantity']

class OrdersForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer','complete','transaction_id']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','owner','price','digital','image','category','rating']

class AddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['customer', 'order', 'address', 'city', 'state', 'zipcode']

