from django.shortcuts import render
from django.views import View


class Index(View):
    def __init__(self):
        pass

    def get(self, request):
        data = {}
        return render(request, 'shop/index.html', {'data': data})

    def post(self, request):
        pass


class AddProduct(View):
    def __init__(self):
        pass

    def get(self, request):
        pass

    def post(self, request):
        pass