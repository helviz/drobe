from django.shortcuts import render,redirect,get_object_or_404
from authentication.models import Business, Customer, Profile
from .forms import *
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash,authenticate,login
from shop.models import Category,OrderItem,Order,Product,ShippingAddress
from django.contrib import messages
from authentication.forms import UserLoginForm, UserCreationForm

def customlogin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_page')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = UserLoginForm()
    return render(request, 'Admin_dashboard/customlogin.html', {'form': form})

def newuser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customlogin')
    else:
        form = UserCreationForm()
    return render(request, 'Admin_dashboard/newuser.html', {'form': form})


def admin_page(request):
    return render(request, "Admin_dashboard/admin_page.html")

def business_list(request):
    businesses = Business.objects.all()
    return render(request, "Admin_dashboard/business_list.html", {'businesses': businesses})

def business_detail(request, pk):
    business = get_object_or_404(Business, pk=pk)
    return render(request, 'Admin_dashboard/business_list.html', {'business': business})

def business_edit(request,business_id):
    business = get_object_or_404(Business, id=business_id)
    if request.method == 'POST':
        form = BusinessForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            return redirect('business_list')  # Redirect to category list page or any other page
    else:
        form = BusinessForm(instance=business)
    
    return render(request, 'Admin_dashboard/business_edit.html', {'form': form, 'business': business})

def customer_edit(request,customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')  # Redirect to category list page or any other page
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'Admin_dashboard/customer_edit.html', {'form': form, 'customer': customer})


def business_create(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('business_list')
    else:
        form = BusinessForm()
    return render(request, 'Admin_dashboard/business_create.html', {'form': form})

def business_delete(request, pk):
    business = get_object_or_404(Business, pk=pk)
    if request.method == 'POST':
        business.delete()
        return redirect('business_list')
    return render(request, 'Admin_dashboard/business_delete.html', {'businesses': business})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "Admin_dashboard/customer_list.html", {'customers': customers})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'Admin_dashboard/customer_detail.html', {'customer': customer})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'Admin_dashboard/customer_create.html', {'form': form})

def customer_delete(request, pk):
    customers = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customers.delete()
        return redirect('customer_list')
    return render(request, 'Admin_dashboard/customer_delete.html', {'customers': customers})

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, "Admin_dashboard/profile_list.html", {'profiles': profiles})

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'profile_detail.html', {'profile': profile})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'Admin_dashboard/customer_create.html', {'form': form})

def customer_delete(request, pk):
    customers = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customers.delete()
        return redirect('profile_list')
    return render(request, 'Admin_dashboard/customer_delete.html', {'customers': customers})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "Admin_dashboard/customer_list.html", {'customers': customers})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customer_detail.html', {'customer': customer})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'Admin_dashboard/customer_create.html', {'form': form})

def customer_delete(request, pk):
    customers = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customers.delete()
        return redirect('customer_list')
    return render(request, 'Admin_dashboard/customer_delete.html', {'customers': customers})

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, "Admin_dashboard/profile_list.html", {'profiles': profiles})

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'profile_detail.html', {'profile': profile})

def profile_create(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = ProfileForm()
    return render(request, 'Admin_dashboard/profile_create.html', {'form': form})

def profile_delete(request, pk):
    profiles = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        profiles.delete()
        return redirect('profile_list')
    return render(request, 'Admin_dashboard/profile_delete.html', {'profiles': profiles})
    

def user_details(request):
    users = User.objects.all()
    return render(request, 'Admin_dashboard/user_details.html', {'users': users})

def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_details')  
    else:
        form = UserCreationForm()

    return render(request, 'Admin_dashboard/add_user.html', {'form': form})

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            update_session_auth_hash(request, user)  
            return redirect('user_details') 
    else:
        user_form = UserChangeForm(instance=user)
        password_form = PasswordChangeForm(user)
    
    return render(request, 'Admin_dashboard/edit_user.html', {'user_form': user_form, 'password_form': password_form, 'user': user})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'Admin_dashboard/category_list.html', {'categories': categories})

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Redirect to category list page or any other page
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'Admin_dashboard/edit_category.html', {'form': form, 'category': category})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'Admin_dashboard/category_create.html', {'form': form})

def items_list(request):
    items = OrderItem.objects.all()
    return render(request, 'Admin_dashboard/items_list.html', {'items': items})

def edit_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('items_list')  
    else:
        form = OrderItemForm(instance=item)
    
    return render(request, 'Admin_dashboard/edit_item.html', {'form': form, 'item': item})


def create_item(request):
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items_list')
    else:
        form = OrderItemForm()
    return render(request, 'Admin_dashboard/create_item.html', {'form': form})

def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'Admin_dashboard/orders_list.html', {'orders': orders})

def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrdersForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders_list')  
    else:
        form = OrdersForm(instance=order)
    
    return render(request, 'Admin_dashboard/view_order.html', {'form': form, 'order': order})

def create_order(request):
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orders_list')
    else:
        form = OrdersForm()
    return render(request, 'Admin_dashboard/create_order.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, "Admin_dashboard/product_list.html", {'products': products})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'Admin_dashboard/edit_product.html', {'form': form, 'product': product})

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'Admin_dashboard/create_product.html', {'form': form})

def address_list(request):
    addresses = ShippingAddress.objects.all()
    return render(request,'Admin_dashboard/address_list.html',{'addresses': addresses})

def create_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('address_list')
    else:
        form = AddressForm()
    return render(request, 'Admin_dashboard/create_address.html', {'form': form})

def edit_address(request,address_id):
    address = get_object_or_404(ShippingAddress,id=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('address_list')  
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'Admin_dashboard/edit_address.html', {'form': form, 'address': address})
