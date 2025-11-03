from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Brand, Product, ProductVariant, Discount, ProductReview, Category
from .forms import BrandForm, ProductForm, ProductVariantForm, DiscountForm, ProductReviewForm


from django.views.generic import TemplateView
from django.db.models import Q
from .models import Product, Discount, Brand, Category


class HomePageView(TemplateView):
    template_name = 'dashboard/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Carousel: first 3 products
        context['carousel_products'] = Product.objects.all()[:3]

        # Group 1: Men’s & Women’s Clothing
        context['men_women_products'] = Product.objects.filter(
            Q(category=Category.MENS_CLOTHING) | Q(category=Category.WOMENS_CLOTHING)
        )[:12]  # limit to 12 for homepage

        # Group 2: Discounted Products
        all_discounts = Discount.objects.filter(active=True)
        discounted_products = []
        for product in Product.objects.all():
            if any(d.applies_to_product(product) for d in all_discounts):
                discounted_products.append(product)
        context['discounted_products'] = discounted_products[:12]

        # Group 3: Others (everything not in men/women or discounted)
        excluded_ids = [p.id for p in context['men_women_products']] + [p.id for p in discounted_products]
        context['other_products'] = Product.objects.exclude(id__in=excluded_ids)[:12]

        # Categories: instead of brands, let’s keep it to Category enums for navigation
        context['categories'] = Category.choices

        return context





# BRAND VIEWS
class BrandListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Brand
    template_name = 'dashboard/brands/brand_list.html'
    context_object_name = 'brands'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs


class BrandCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Brand
    form_class = BrandForm
    template_name = 'dashboard/brands/brand_form.html'
    success_url = reverse_lazy('brand-list')


class BrandUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Brand
    form_class = BrandForm
    template_name = 'dashboard/brands/brand_form.html'
    success_url = reverse_lazy('brand-list')


class BrandDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Brand
    template_name = 'dashboard/brands/brand_confirm_delete.html'
    success_url = reverse_lazy('brand-list')


# PRODUCT VIEWS
class ProductListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Product
    template_name = 'dashboard/products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        brand = self.request.GET.get('brand')
        category = self.request.GET.get('category')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        q = self.request.GET.get('q')

        if brand:
            qs = qs.filter(brand__id=brand)
        if category:
            qs = qs.filter(category=category)
        if price_min:
            qs = qs.filter(price__gte=price_min)
        if price_max:
            qs = qs.filter(price__lte=price_max)
        if q:
            qs = qs.filter(name__icontains=q)

        return qs


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/products/product_form.html'
    success_url = reverse_lazy('product-list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/products/product_form.html'
    success_url = reverse_lazy('product-list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Product
    template_name = 'dashboard/products/product_confirm_delete.html'
    success_url = reverse_lazy('product-list')


# PRODUCT VARIANT VIEWS
class ProductVariantListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = ProductVariant
    template_name = 'dashboard/variants/variant_list.html'
    context_object_name = 'variants'

    def get_queryset(self):
        self.product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return ProductVariant.objects.filter(product=self.product)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        return context


class ProductVariantCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = ProductVariant
    form_class = ProductVariantForm
    template_name = 'dashboard/variants/variant_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['product'].widget = forms.HiddenInput()
        return form

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        form.instance.product = product
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('product-variants', kwargs={'pk': self.kwargs['pk']})


class ProductVariantUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = ProductVariant
    form_class = ProductVariantForm
    template_name = 'dashboard/variants/variant_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['product'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context

    def get_success_url(self):
        product_pk = self.kwargs.get('product_pk') or self.object.product.pk
        return reverse_lazy('product-variants', kwargs={'pk': product_pk})


class ProductVariantDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = ProductVariant
    template_name = 'dashboard/variants/variant_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context

    def get_success_url(self):
        product_pk = self.kwargs.get('product_pk') or self.object.product.pk
        return reverse_lazy('product-variants', kwargs={'pk': product_pk})


# DISCOUNT VIEWS
class DiscountListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Discount
    template_name = 'dashboard/discounts/discount_list.html'
    context_object_name = 'discounts'


class DiscountCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Discount
    form_class = DiscountForm
    template_name = 'dashboard/discounts/discount_form.html'
    success_url = reverse_lazy('discount-list')


class DiscountUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Discount
    form_class = DiscountForm
    template_name = 'dashboard/discounts/discount_form.html'
    success_url = reverse_lazy('discount-list')


class DiscountDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Discount
    template_name = 'dashboard/discounts/discount_confirm_delete.html'
    success_url = reverse_lazy('discount-list')

@method_decorator(login_required, name='dispatch')  # Require login for POST
class ProductDetailView(DetailView):
    model = Product
    template_name = 'dashboard/pages/product_detail.html'
    context_object_name = 'product'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Variants
        context['variants'] = product.variants.all()

        # Approved Reviews
        reviews_qs = product.reviews.filter(approved=True)
        context['reviews'] = reviews_qs

        # Rating statistics
        total_reviews = reviews_qs.count()
        avg_rating = reviews_qs.aggregate(Avg('rating'))['rating__avg'] or 0

        # Count reviews per rating (1-5)
        rating_counts = reviews_qs.values('rating').annotate(count=Count('rating')).order_by('-rating')

        # Create a dictionary for an easy lookup
        rating_dict = {item['rating']: item['count'] for item in rating_counts}

        # Prepare data for all ratings (5 down to 1)
        rating_stats = []
        for rating in range(5, 0, -1):
            count = rating_dict.get(rating, 0)
            rating_stats.append({
                'rating': rating,
                'count': count
            })

        context['rating_stats'] = rating_stats
        context['total_reviews'] = total_reviews
        context['avg_rating'] = round(avg_rating, 1)

        # Active discounts
        context['discounts'] = product.get_active_discounts()

        # Discounted price
        context['discounted_price'] = product.get_discounted_price()

        # Related products
        related = Product.objects.filter(brand=product.brand).exclude(id=product.id)[:4]
        if not related.exists() and product.category:
            related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
        context['related_products'] = related

        # Review form
        context['review_form'] = ProductReviewForm(product=product)
        return context

    def post(self, request, *args, **kwargs):
        """Handle review submission from logged-in users"""
        product = self.get_object()
        form = ProductReviewForm(request.POST, product=product)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', pk=product.pk)
        # If form is invalid, re-render the page with form errors
        context = self.get_context_data()
        context['review_form'] = form
        return self.render_to_response(context)

class ProductsListView(ListView):
    model = Product
    template_name = "dashboard/pages/product_list.html"
    context_object_name = "products"
    paginate_by = 12  # 12 products per page

    def get_queryset(self):
        queryset = Product.objects.all().order_by("-created_at")

        # Search
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

        # Filter by category
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)

        # Filter by brand
        brand = self.request.GET.get("brand")
        if brand:
            queryset = queryset.filter(brand__id=brand)

        # Price filter
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        if "page" in params:
            params.pop("page")
        context["querystring"] = params.urlencode()
        context["brands"] = Brand.objects.all()
        context["categories"] = Category.choices
        context["selected_category"] = self.request.GET.get("category", "")
        context["selected_brand"] = self.request.GET.get("brand", "")
        context["search_query"] = self.request.GET.get("q", "")
        return context

