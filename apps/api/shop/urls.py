from django.urls import path
from . import shop

urlpatterns = [
    path('suggestions/', shop.IndexProduct.as_view(), name='suggestions'),
    path('addproduct/', shop.AddProduct.as_view(), name='addproduct'),
    path('showproduct/<int:id>', shop.ShowProduct.as_view(), name='showproduct'),
]