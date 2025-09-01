from django.shortcuts import render, redirect
# from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.views import LoginView

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()           
            return redirect('login')
        
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})

class UserLoginView(LoginView):
    template_name = 'users/login.html'
