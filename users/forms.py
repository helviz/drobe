from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone number'}))
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY', 'type': 'date'})
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'phone_number', 'date_of_birth', 'password1', 'password2']
