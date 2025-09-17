from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'phone_number', 'date_of_birth')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'phone_number', 'date_of_birth')  # keep password out
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    # Exclude the password field entirely
    password = None
