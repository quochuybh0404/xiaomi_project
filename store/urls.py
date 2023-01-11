from django.urls import path
from store.views import *

app_name = 'store'
urlpatterns = [
    path('', index, name = 'index'),
    path('contact/', contact, name = 'contact'),
    path('shop-details/<int:pk>/', shop_details, name = 'shop_details'),
    path('shop-grid/<int:pk>/', shop_grid, name = 'shop_grid'),
    path('search/', search, name = 'search'),
]