from django.shortcuts import render
from django.views import View


class NotifView(View):
    def get(self, request):
        data = {}
        return render(request, 'notifications/notif.html', {'data': data})

    def post(self, request):
        pass

