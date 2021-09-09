from django.shortcuts import render
from django.views import View


class SettingsIndexView(View):
    def get(self, request):
        data = {}
        return render(request, 'settings/index.html', {'data': data})

    def post(self, request):
        pass