from django import forms
from .models import Brand, Product, ProductVariant, Discount, ProductReview, Category


# BRAND FORM
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'image']


# PRODUCT FORM
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'price', 'description', 'image', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


# PRODUCT VARIANT FORM
class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product', 'size','color', 'stock', 'image']
        widgets = {
            'stock': forms.NumberInput(attrs={'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].required = False


# DISCOUNT FORM
class DiscountForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(
        choices=Category.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Discount
        fields = [
            'name', 'discount_type', 'value', 'start_date', 'end_date',
            'active', 'products', 'brands', 'categories', 'priority'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'products': forms.CheckboxSelectMultiple(),
            'brands': forms.CheckboxSelectMultiple(),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }




# PRODUCT REVIEW FORM
class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['variant', 'rating', 'comment']  # Removed 'product' and 'approved'
        widgets = {
            'variant': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if product:
            # Only show variants for this product
            self.fields['variant'].queryset = product.variants.all()
        else:
            self.fields['variant'].queryset = ProductVariant.objects.none()
        self.fields['variant'].required = False