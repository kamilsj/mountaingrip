from locale import currency
from django.db import models
from django.contrib.auth.models import User


PURCHASE_STATUS = [
    ('P', 'Pending'),
    ('C', 'Completed'),
    ('X', 'Cancelled'),    
]

class Brand(models.Model):
    name = models.CharField(max_length=256, blank=False)
    logo = models.ImageField(upload_to='brands', blank=True, null=True)
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
    price = models.FloatField(default=0)
    currency = models.CharField(max_length=3, default='PLN')
    quantity = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_image_author", blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images", blank=False)
    image = models.ImageField(upload_to='products', blank=False)


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchase_user", blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchase_product", blank=False)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=1, choices=PURCHASE_STATUS, default='P')
    added_at = models.DateTimeField(auto_now_add=True)




