from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class ImageChoice(models.TextChoices):
    NOT_ATTEMPTED               =  '00', _('NOT_ATTEMPTED')
    CATEGORY                     =  '01', _('CATEGORY')
    SUBCATEGORY                   =  '02', _('SUBCATEGORY')
    PRODUCT                  =  '03', _('PRODUCT')

 
class User(AbstractUser):
    name  =    models.CharField(max_length=255)
    email  =    models.CharField(max_length=255)
    mobile  =    models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.name}, {self.mobile}"

class Address(models.Model):
    street = models.CharField(max_length=255)
    city     = models.CharField(max_length=255)
    state    = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}------{self.zip_code}"


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    addresses = models.ManyToManyField(Address)

    def __str__(self):
        return f"{self.user.name}"
 
    
class Merchant(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    website  =    models.CharField(max_length=255)
    addresses = models.ManyToManyField(Address)
    
    def __str__(self):
        return f"{self.user.email}, {self.user.name}"
    
class ProductImages(models.Model):
    CATEGORY = 'category'
    SUBCATEGORY = 'subcategory'
    PRODUCT = 'product'
    NONE= 'None'

    IMAGE_TYPES = [
        (CATEGORY, 'Category'),
        (SUBCATEGORY, 'Subcategory'),
        (PRODUCT, 'Product'),
        (NONE, 'NONE'),
    ]
    
    image=models.TextField()
    image_url=models.TextField(null=True)
    image_file=models.FileField(upload_to="media/images",null=True)
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES,default=NONE)

    def __str__(self):
        return f"{self.image_type}"
    
    


class ProductCategory(models.Model):
    category=models.CharField(max_length=255)
    image=models.ManyToManyField(ProductImages)

    def __str__(self):
        return f"{self.category}"

class SubCategory(models.Model):
    name=models.CharField(max_length=255)
    category=models.ForeignKey(ProductCategory,on_delete=models.CASCADE,null=True)
    image=models.ManyToManyField(ProductImages)

    def __str__(self):
        return f"{self.name}------{self.category}"
    
    
class Products(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_percent = models.FloatField()
    images = models.ManyToManyField(ProductImages)
    seller = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    brand = models.CharField(max_length=255,null=True)
    stock = models.CharField(max_length=255,null=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    highlights = models.TextField(null=True)
    unique_id=models.UUIDField(null=True)
    verified=models.BooleanField(default=False)
    reviews_count = models.CharField(max_length=255,null=True)
    avg_rating = models.CharField(max_length=255,null=True)
    subcategory2=  models.CharField(max_length=255,null=True)

    def __str__(self):
        return f"{self.name}------{self.category}"
    
    
    

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField('Book name', max_length=100)
    author = models.ForeignKey(Author, blank=True, null=True,on_delete=models.CASCADE)
    author_email = models.EmailField('Author email', max_length=75, blank=True)
    imported = models.BooleanField(default=False)
    published = models.DateField('Published', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name