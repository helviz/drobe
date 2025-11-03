from . import views
from django.urls import path
from .views import (
    BrandListView, BrandCreateView, BrandUpdateView, BrandDeleteView,
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    ProductVariantListView, ProductVariantCreateView, ProductVariantUpdateView, ProductVariantDeleteView,
    DiscountListView, DiscountCreateView, DiscountUpdateView, DiscountDeleteView,HomePageView, ProductDetailView,
    ProductsListView,
)

urlpatterns = [
    # Dashboard
    path('', HomePageView.as_view(), name='dashboard'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path("products/", ProductsListView.as_view(), name="all_products_list"),

    # Brands
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('brands/add/', BrandCreateView.as_view(), name='brand-add'),
    path('brands/<int:pk>/edit/', BrandUpdateView.as_view(), name='brand-edit'),
    path('brands/<int:pk>/delete/', BrandDeleteView.as_view(), name='brand-delete'),

    # Products
    path('products-list/', ProductListView.as_view(), name='product-list'),
    path('products/add/', ProductCreateView.as_view(), name='product-add'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product-edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    # Product Variants
    path('products/<int:pk>/variants/', ProductVariantListView.as_view(), name='product-variants'),
    path('products/<int:pk>/variants/add/', ProductVariantCreateView.as_view(), name='variant-add'),
    path('products/<int:product_pk>/variants/<int:pk>/edit/', ProductVariantUpdateView.as_view(), name='variant-edit'),
    path('products/<int:product_pk>/variants/<int:pk>/delete/', ProductVariantDeleteView.as_view(), name='variant-delete'),

    # Discounts
    path('discounts/', DiscountListView.as_view(), name='discount-list'),
    path('discounts/add/', DiscountCreateView.as_view(), name='discount-add'),
    path('discounts/<int:pk>/edit/', DiscountUpdateView.as_view(), name='discount-edit'),
    path('discounts/<int:pk>/delete/', DiscountDeleteView.as_view(), name='discount-delete'),

]
