from django.urls import path
from customer.views import *

app_name = 'customer'
urlpatterns = [
    path('register/', customer_register, name = 'customer_register'), 
    path('login/', customer_login, name = 'customer_login'),
    path('logout/', customer_logout, name = 'customer_logout'),
    path('my-account/', my_account, name = 'my_account'),
    path('reset-password', reset_password, name ='reset_password'),
]