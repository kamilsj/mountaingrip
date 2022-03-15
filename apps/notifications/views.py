from django.shortcuts import render, redirect
from django.views import View


class NotifView(View):
    def get(self, request):
        if request.user.is_authenticated:  
            data = {}
            return render(request, 'notifications/notif.html', {'data': data})
        else:
            return redirect('/')

    def post(self, request):
        pass

