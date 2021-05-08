from django.shortcuts import render
from django.views import View


class Index(View):
    def get(self, request):
        data = {}
        return render(request, 'ranking/index.html', {'data': data})

    def post(self, request):
        pass
