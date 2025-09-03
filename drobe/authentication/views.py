from django.shortcuts import render, redirect
from django.http import JsonResponse
from shop.utilities import cartData
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
import json, uuid
from django.contrib import messages
from shop.utilities import send_message
import threading, time
from django.views.decorators.csrf import csrf_exempt
import hashlib
from django.conf import settings
from django.contrib import messages
from rest_framework.decorators import api_view


sender_email = settings.EMAIL_HOST_USER
sender_password = settings.EMAIL_HOST_PASSWORD


# View for displaying user profile
@login_required
@api_view(["GET", "POST"])
def profile(request):
    # Fetch cart data for the user
    data = cartData(request)
    cartItems = data["cartItems"]
    business_owner = ""
    products = []

    try:
        the_user = Customer.objects.filter(user=request.user).first()
        if len(Customer.objects.filter(user=request.user)) == 0:
            raise ValueError
        orders_ = Order.objects.filter(customer=request.user).order_by("-date_ordered")
        orders = []
        for order in orders_:
            if order.transaction_id:
                orders.append(order)
        the_user = "Customer"

    except Exception as e:
        the_user = "Business"
        business = Business.objects.filter(owner=request.user).first()
        products = Product.objects.filter(owner=business)
        orderitems = OrderItem.objects.filter(product__owner=business).order_by("-date_added")
        orders = []
        for orderitem in orderitems:
            if orderitem.order not in orders and orderitem.order.transaction_id:
                orders.append(orderitem.order)
        
        business_owner = business
        
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            try:
                customer = Customer.objects.filter(user=request.user).first()
                customer.first_name = f"{user_form.cleaned_data.get('first_name')}"
                customer.last_name = f"{user_form.cleaned_data.get('last_name')}"
                customer.email = f"{user_form.cleaned_data.get('email')}"
                customer.save()
            except Exception as e:
                business = Business.objects.filter(owner=request.user).first()
                business.first_name = f"{user_form.cleaned_data.get('first_name')}"
                business.last_name = f"{user_form.cleaned_data.get('last_name')}"
                business.email = f"{user_form.cleaned_data.get('email')}"
                business.save()
            
            return redirect("profile")
            
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = UserUpdateForm(instance=request.user)

    
    # Context for rendering the profile page
    context={
        'title':'PROFILE',
        'cartItems':cartItems,
        'profile_form': profile_form,
        'user_form': user_form,
        'orders': orders,
        'the_user': the_user, 
        'business_owner': business_owner, 
        'products': products, 
        'first_order': orders[0] if orders else 0
        }

    return render(request, "authentication/profile.html",context)  

# View for handling user login
def login_user(request):
    # Fetch cart data for the user
    data = cartData(request)
    cartItems = data["cartItems"]
    
    # If the request method is POST (form submission)
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Log in user and redirect to the home page
                login(request, user)
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("home")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = UserLoginForm()
    
    # Context for rendering the login page
    context={
        'title':'LOGIN',
        'cartItems':cartItems,
        'form':form
        }
    
    # Render the login page
    return render(request, "authentication/login.html", context)

#delete unverified users
def delete_unverified_user(user):
    time.sleep(60 * 60 * 24)
    try:
        if not user.verified:
            user.delete()
            print("The user has been deleted")
    except:
        print("The user wasn't found.")

#verify users
@csrf_exempt
def verify(request, token):
    customer = Customer.objects.filter(token=token).first()
    business = Business.objects.filter(token=token).first()
    if customer:
        customer.verified = True
        customer.save()
        messages.success(request, "Account successfully activated.")
        return redirect("shop")
    elif business:
        if business:
            business.verified = True
            business.save()
            messages.success(request, "Account successfully activated.")
        return redirect("profile")
    
    messages.error(request, "The provided link seems to be invalid.")
    return redirect("login")
        
      
        
# View for handling user signup
def signup_user(request):
    # Fetch cart data for the user
    data = cartData(request)
    cartItems = data["cartItems"]
    host = request.get_host()
   
    if request.POST:
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            # Save user registration form
            form.save()
            user = User.objects.filter(username=form.cleaned_data.get("username")).first()
            delete_thread = threading.Thread(target=delete_unverified_user, args=(user, ), daemon=True)
            delete_thread.start()
            # Create a corresponding customer profile
            customer = Customer.objects.create(user=user,first_name=user.first_name,last_name=user.last_name, email=user.email)
            text = user.username + customer.first_name + customer.last_name + customer.email
            hashed_text = hashlib.md5(text.encode()).hexdigest()
            token = uuid.UUID(hashed_text)
            customer.token = token
            customer.save()
            send_message(customer.first_name, customer.email, token, host, sender_email,sender_password)
            Profile.objects.create(user=user)
            messages.success(request, "The account was successfully created but you need to activate it within 24 hours or it will be deleted.")
            return redirect("login")
        else:
            messages.error(request, "Please the check the details you entered.")
    else:
        form = CustomerRegisterForm()
        print("some errors")
    # Context for rendering the user signup page
    context={
        'title':'SIGNUP',
        'cartItems':cartItems,
        'form':form
        }
    
    # Render the user signup page
    return render(request, "authentication/signup-user.html", context)    

# View for handling business signup
def signup_business(request):
    try:
        signup_data = json.loads(request.body)
    except:
        signup_data = {}
        
    data = cartData(request)
    cartItems = data["cartItems"]
    host = request.get_host()
    
    
    if signup_data:
        customer_form = CustomerRegisterForm(signup_data['form'])
        business_form = BusinessRegisterForm(signup_data['form'])
        
        if customer_form.is_valid() and business_form.is_valid():
            # Save user registration forms
            customer_form.save()
            user  = User.objects.filter(username=signup_data['form'].get("username")).first()
            delete_thread = threading.Thread(target=delete_unverified_user, args=(user, ), daemon=True)
            delete_thread.start()
            business = Business.objects.create(owner=user,business_name=signup_data['form'].get("business_name"),first_name=user.first_name,last_name=user.last_name, email=user.email)
            text = user.username + business.first_name + business.last_name + business.email
            hashed_text = hashlib.md5(text.encode()).hexdigest()
            token = uuid.UUID(hashed_text)
            business.token = token
            business.save()
            Profile.objects.create(user=user)
            send_message(business.first_name, business.email, token, host, sender_email, sender_password)
            return JsonResponse("Business was created.", safe=False)
        else:
            messages.error(request, "There was an issue with those details, if you followed all instructions then that company is already registered.")
            return JsonResponse("Business was not created.", safe=False)
    else:
        customer_form = CustomerRegisterForm()
        business_form = BusinessRegisterForm()
        print("some errors")
        
    # Context for rendering the business signup page
    context={
        'title':'SIGNUP',
        'cartItems':cartItems,
        'customer_form':customer_form,
        'business_form':business_form
        }
    
    # Render the business signup page
    return render(request, "authentication/signup-business.html", context)    

# View for handling user logout
def logout_u(request):
    # Log out the user and redirect to the home page
    logout(request)
    return redirect("home")

@login_required
def add_products(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    
    if request.method == 'POST':
        form = BusinessAddProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            product = Product.objects.filter(name=request.POST.get("name"), price=request.POST.get("price"), description=request.POST.get("description"), category=request.POST.get("category")).first()
            business = Business.objects.filter(owner=request.user).first()
            product.owner = business
            product.save()
            return redirect("shop")
    else:
        form = BusinessAddProductsForm()
        
    context={
        'title':'ADD PRODUCTS',
        'cartItems':cartItems,
        'form':form
        }
    return render(request, "authentication/add-products.html", context)



