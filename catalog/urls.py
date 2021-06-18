from django.urls import path
from .views import (
    HomeView,
    CheckoutView,
    ProductDetail,
    OrderSummaryView,
    PaymentView,
    add_to_cart,
    remove_from_cart,
    remove_single_from_cart
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove-single-from-cart/<slug>/', remove_single_from_cart, name='remove_single_from_cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('product/<slug>/', ProductDetail.as_view(), name='product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>', PaymentView.as_view(), name='payment')
]