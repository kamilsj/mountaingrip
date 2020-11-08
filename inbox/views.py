from django.shortcuts import render
from django.views import View


class Inbox(View):
    def get(self, request):
        data = {}
        return render(request, 'inbox/inbox.html', {'data': data})

    def post(self, request):
        pass

