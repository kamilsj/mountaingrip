from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from .forms import ProductForm
from .models import Product, Brand, Category, Purchase
import stripe
import requests


class Index(View):
 
    
    def get(self, request):
        if request.user.is_authenticated:
            data = {}
            if request.session['beta'] is True and settings.BETA is True:
                products = Product.objects.exclude(user=request.user).all()[:25]

                data = {
                    'products': products,
                }
                

            else:
                data = {'info': 'Space only for beta testers. For now.'}
            return render(request, 'shop/index.html', {'data': data})
        else:
            return redirect('/')

    def post(self, request):
        pass


class Purchases(View):
    def get(self, request):
        if request.user.is_authenticated:            
            data = {}
            if request.session['beta'] is True and settings.BETA is True:
                purchases = Purchase.objects.exclude(user=request.user).all()[:25]
                data = {
                    'purchases': purchases,
                }
            else:
                data = {'info': 'Space only for beta testers. For now.'}
            return render(request, 'shop/purchases.html', {'data': data})
        else:
            return redirect('/')

    def post(self, request):
        pass


class ShowProduct(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if id > 0:
                product = Product.objects.get(id=id)
                data = {
                    'product': product,
                }
                return render(request, 'shop/show_product.html', {'data': data})
        else:
            return redirect('/')

    def post(self, request):
        pass

class AddProduct(View):
    form_class = ProductForm
    def get(self, request):
        if request.user.is_authenticated:
            data = {}
            if request.session['beta'] is True and settings.BETA is True:
                #ok beta testing works fine
                
                data = {
                    'categories': Category.objects.all(),
                    'brands': Brand.objects.order_by('name').all(),
                }

            else:
                data = {'info': 'Space only for beta testers. For now.'}
            return render(request, 'shop/add_product.html', {'data': data, 'form': self.form_class})
        else:
            return redirect('/')

    def post(self, request):
        if request.user.is_authenticated:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.user = request.user
                obj = product.save()
                return redirect('/shop/'+str(obj.id))
            else:
                return render(request, 'shop/add_product.html', {'form': form})
        else:
            return redirect('/')