from django import forms
from .models import Product, Category
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput

class ProductForm(forms.ModelForm):
    pic = forms.ImageField(required=False, widget=ClearableFileInput(attrs={'allow_multiple_selected': True}))
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'brand', 'category', 'quantity', 'pic']