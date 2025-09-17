from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.views import LoginView, LogoutView



# Registration view
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    LOGIN_REDIRECT_URL = 'dashboard'


@login_required
def profile_view(request):
    global profile_form, password_form
    user = request.user

    if request.method == 'POST':
        # Determine which form is submitted
        if 'update_profile' in request.POST:
            profile_form = CustomUserChangeForm(request.POST, instance=user)
            password_form = PasswordChangeForm(user)  # empty form
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('profile')
        elif 'update_password' in request.POST:
            profile_form = CustomUserChangeForm(instance=user)  # empty form
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # keeps the user logged in
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
    else:
        profile_form = CustomUserChangeForm(instance=user)
        password_form = PasswordChangeForm(user)

    context = {
        'form': profile_form,
        'password_form': password_form
    }
    return render(request, 'profile/profile.html', context)

