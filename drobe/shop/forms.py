from django import forms
from .models import ShippingAddress
from django.utils.safestring import mark_safe
class ShippingAddressForm(forms.ModelForm):
    address = forms.CharField(required=True, label="Address")
    city = forms.CharField(required=True, label="City")
    state = forms.CharField(required=True, label="State")
    zipcode = forms.CharField(required=True, label="Zipcode")
    
    class Meta:
        model = ShippingAddress
        fields = ["address", "city", "state", "zipcode"]
        
    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: red;'>*</span>")



class UserInfoForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly', 'class':'form-control'}), label="First Name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly', 'class':'form-control'}), label= "Last Name")
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly', 'class':'form-control'}), label = "Email")
    
    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in self.Meta.required_fields:
                field.label = mark_safe(f"{field.label} <span style='color: red;'>*</span>")

    class Meta:
        required_fields = ["first_name", "last_name", "email"]

    
    