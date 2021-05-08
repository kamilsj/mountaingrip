from django.shortcuts import render
from django.views import View
from django.conf import settings

class Inbox(View):
    def get(self, request):
        data = {}
        if settings.BETA == True and request.session['beta'] == True:
            pass
        else:
            data = {'info': 'You cannot be here. Space only for beta testers ;).'}
        return render(request, 'inbox/inbox.html', {'data': data})

    def post(self, request):
        pass


class NewMessage(View):
    def get(self, request):
        pass

    def post(self, request):
        pass

