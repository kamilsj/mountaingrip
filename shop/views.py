from django.shortcuts import render
from django.views import View
from django.conf import settings


class Index(View):

    def get(self, request):
        data = {}
        if request.session['beta'] == True and settings.BETA == True:
            #ok beta testing works fine
            pass

        else:
            data = {'info': 'Space only for beta testers. For now.'}
        return render(request, 'shop/index.html', {'data': data})

    def post(self, request):
        pass


class AddProduct(View):

    def get(self, request):
        pass

    def post(self, request):
        pass