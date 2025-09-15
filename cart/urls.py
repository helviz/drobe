from django.urls import path
from . import views

urlpatterns = [
    path('detail/', views.cart_detail, name='cart_detail'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process_order/', views.process_order, name='process_order'),
    path('my-orders/', views.order_list, name='order-list'),
]
