from django.shortcuts import render
from django.views import View
from django.conf import settings


class Index(View):

    def get(self, request):
        data = {}
        if request.session['beta'] is True and settings.BETA is True:
            #ok beta testing works fine
            pass

        else:
            data = {'info': 'Space only for beta testers. For now.'}
        return render(request, 'shop/index.html', {'data': data})

    def post(self, request):
        pass


class Purchases(View):
    def get(self, request):
        data = {}
        if request.session['beta'] is True and settings.BETA is True:
            # ok beta testing works fine
            pass

        else:
            data = {'info': 'Space only for beta testers. For now.'}
        return render(request, 'shop/purchases.html', {'data': data})

    def post(self, request):
        pass


class AddProduct(View):

    def get(self, request):
        data = {}
        if request.session['beta'] is True and settings.BETA is True:
            #ok beta testing works fine
            pass

        else:
            data = {'info': 'Space only for beta testers. For now.'}
        return render(request, 'shop/add_product.html', {'data': data})

    def post(self, request):
        pass