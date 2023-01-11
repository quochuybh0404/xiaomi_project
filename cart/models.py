from django.db import models
from django.db import models
from customer.models import Customer
from store.models import Product

# Create your models here.
class OrderConfirm(models.Model):
    first_name = models.CharField(max_length=200, blank= False)
    last_name = models.CharField(max_length=200, blank= False)
    address = models.TextField()
    email = models.EmailField(blank=False)
    tel = models.CharField(max_length=15)

    def __str__(self):
        return self.last_name + ' ' + self.first_name 


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.PROTECT)
    total = models.DecimalField(max_digits = 10, decimal_places= 2)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created'] # sort theo cái ngày đặt hàng. Ngày mới đặt luôn được nằm ở trên

    def __str__(self):
        return f'Order {self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete= models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.pk)