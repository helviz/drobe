from django import forms
from django.contrib import admin
from .models import Brand, Product, ProductVariant, Discount, ProductReview, Category


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)



class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ('size', 'color', 'stock', 'image')
    readonly_fields = ('created_at',)


class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    fields = ('user', 'variant', 'rating', 'comment', 'approved')
    readonly_fields = ('created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'created_at')
    list_filter = ('brand', 'category', 'created_at')
    search_fields = ('name', 'brand__name')
    inlines = [ProductVariantInline, ProductReviewInline]



@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color',  'stock', 'created_at')
    list_filter = ('product', 'size', 'color')
    search_fields = ('product__name', 'size', 'color')



class DiscountForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(
        choices=Category.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Discount
        fields = '__all__'

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    form = DiscountForm
    list_display = ('name', 'discount_type', 'value', 'active', 'start_date', 'end_date')
    list_filter = ('discount_type', 'active', 'start_date', 'end_date')
    search_fields = ('name',)
    filter_horizontal = ('products', 'brands')


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'variant', 'rating', 'approved', 'created_at')
    list_filter = ('approved', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'variant__size', 'variant__color')
