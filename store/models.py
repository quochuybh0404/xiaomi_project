from django.db import models

# Create your models here.
from unicodedata import category
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

# Create your models here
class Category(models.Model):
    name = models.CharField(max_length= 150, unique = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete= models.PROTECT)
    name = models.CharField(max_length= 250)
    price = models.FloatField(default= 0.0)
    image = models.ImageField(upload_to = 'store/img', default = 'store/img/logo.png')
    content = RichTextUploadingField(blank = True, null = True)

    def __str__(self):
        return self.name
    

class Contact(models.Model):
    name = models.CharField(max_length= 100)
    email = models.EmailField(blank = False)
    message = models.TextField(blank = False)

    def __str__(self):
        return self.name

