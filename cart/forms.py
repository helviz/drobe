from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["telephone", "destination"]
        widgets = {
            "telephone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter phone number"}),
            "destination": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter delivery address", "rows": 3}),
        }
