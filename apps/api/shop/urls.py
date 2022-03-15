from django.urls import path
from . import shop

urlpatterns = [
    path('addproduct/', shop.AddProduct.as_view(), name='addproduct'),
]