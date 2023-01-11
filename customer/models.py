from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=200, blank= False)
    last_name = models.CharField(max_length=200, blank= False)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=100, blank= False)
    # confirm_password = models.CharField(max_length=100, blank= False)
    tel = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.last_name + ' ' + self.first_name