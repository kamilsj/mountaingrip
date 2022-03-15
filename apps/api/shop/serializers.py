from apps.shop.models import Product, Category, ProductCategory
from rest_framework import serializers

class ProductSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'pic', 'category')