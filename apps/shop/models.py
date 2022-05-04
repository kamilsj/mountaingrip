from locale import currency
from django.db import models
from django.contrib.auth.models import User


PURCHASE_STATUS = [
    ('P', 'Pending'),
    ('C', 'Completed'),
    ('X', 'Cancelled'),    
]

class Brand(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)
    logo = models.ImageField(upload_to='brands', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=4096, blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=4096, blank=True, null=True)
    lang = models.CharField(max_length=2, default='en')


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_author", blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category", blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="product_types", blank=False)
    name = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=4096, blank=True, null=True)
    used = models.IntegerField(choices=[(0, 'Used'), (1, 'New')], default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)      
    discount = models.FloatField(default=0)
    currency = models.CharField(max_length=3, default='PLN')
    quantity = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name+' - '+self.brand.name


class PriceChanges(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='price_changes_user', blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_changes_product', blank=False, null=False)
    price = models.FloatField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    

class ProductImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_image_author", blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images", blank=False)
    image = models.ImageField(upload_to='products', blank=False)


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchase_user", blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchase_product", blank=False)
    quantity = models.PositiveIntegerField(default=0)
    trasactionid = models.CharField(max_length=256, blank=True, null=True)
    status = models.CharField(max_length=1, choices=PURCHASE_STATUS, default='P')
    added_at = models.DateTimeField(auto_now_add=True)




