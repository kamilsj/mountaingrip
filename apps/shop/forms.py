from django import forms
from .models import Product
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput

class ProductForm(forms.ModelForm):
    pic = forms.ImageField(required=False, widget=ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'pic']