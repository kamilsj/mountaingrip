from django.shortcuts import render
from django.views import View


class Group(View):
    def get(self, request):
        data = {}
        return render(request, 'groups/index.html', {'data': data})

    def post(self, request):
        pass


class GroupCreate(View):
    def get (self, request):
        data = {}
        return render(request, 'groups/create.html', {'data': data})

    def post(self, request):
        pass