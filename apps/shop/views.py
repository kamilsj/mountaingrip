from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
import stripe
import requests


class Index(View):
 
    
    def get(self, request):
        if request.user.is_authenticated:
            data = {}
            if request.session['beta'] is True and settings.BETA is True:
                #ok beta testing works fine
                pass

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
                # ok beta testing works fine
                pass

            else:
                data = {'info': 'Space only for beta testers. For now.'}
            return render(request, 'shop/purchases.html', {'data': data})
        else:
            return redirect('/')

    def post(self, request):
        pass


class AddProduct(View):

    def get(self, request):
        if request.user.is_authenticated:
            data = {}
            if request.session['beta'] is True and settings.BETA is True:
                #ok beta testing works fine
                pass

            else:
                data = {'info': 'Space only for beta testers. For now.'}
            return render(request, 'shop/add_product.html', {'data': data})
        else:
            return redirect('/')

    def post(self, request):
        pass