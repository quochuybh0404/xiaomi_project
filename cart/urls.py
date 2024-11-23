from django.urls import path
from cart.views import *

app_name = 'cart'
urlpatterns = [
    path('cart/', cart_detail, name = 'cart_detail'),
    path('update-cart/', update_cart, name='update_cart'),
    path('buy-now/<int:product_id>/', buy_now, name = 'buy_now'),
    # path('cart-add/<int:product_id>/', cart_add, name = 'cart_add'),
    path('remove-cart/<int:product_id>/', remove_cart, name = 'remove_cart'),
    path('checkout/', checkout, name = 'checkout'),
]