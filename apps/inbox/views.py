from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.contrib.auth.models import User

from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _

from func.notif import Notif
from django.db.models import Q

from .forms import MessageForm
from .models import Message


class SentView(View):
    def get(self, request):
        data = {}
        user = request.user
        if settings.BETA is True and request.session['beta'] is True:
            if Message.objects.filter(user=user).count() > 0:
                sent = Message.objects.filter(user=user).order_by('-id').all()[:50]
                data = {
                    'sent': sent
                }
            else:
                data = {'nonew:': _('No sent messages')}
        return render(request, 'inbox/sent.html', {'data': data})

    def post(self, request):
        pass


class MessageView(View):
    def get(self, request, id):
        data = {}
        if id > 0:
            if settings.BETA is True and request.session['beta'] is True:
                if Message.objects.filter(Q(id=id) & (Q(user=request.user) | Q(to=request.user))).exists():
                    message = Message.objects.get(id=id)
                    if message.to.id == request.user.id:
                        message.read = True
                        message.save()
                    conv = message.conversation
                    messages = Message.objects.filter(conversation=conv).exclude(id=id).order_by('-id').all()[:50]
                    if messages.count() > 0:
                        data = {
                            'message': message,
                            'messages': messages
                        }
                    else:
                        data = {
                            'message': message
                        }
                else:
                    return redirect('/inbox/')
        return render(request, 'inbox/message.html', {'data': data})

    def post(self, request, id):
        if request.method == 'POST':
            try:
                message = Message.objects.get(id=id)
                user = message.user
                if message.title[0] != '+':
                    title = '+'+message.title
                else:
                    title = message.title
                conv_id = request.POST['conversation_reply']
                body_text = request.POST['reply_text']
                if message.conversation == conv_id:
                    obj = Message.objects.create(
                        user=request.user,
                        to=user,
                        text=body_text,
                        title=title,
                        conversation=conv_id
                    )

                    return redirect('/inbox/message/'+str(obj.id))
            except Message.DoesNotExist:
                pass


class Inbox(View):
    form_class = MessageForm
    n = Notif(1)

    def get(self, request):
        data = {}
        if settings.BETA is True and request.session['beta'] is True:
            count = Message.objects.filter(to=request.user).count()
            if count > 0:
                messages = Message.objects.filter(to=request.user).order_by('-id').all()[:50]

                data = {
                    'messages': messages,
                }

            else:
                data = {'nonew': _('No messages')}
        else:
            data = {'info': _('You cannot be here. Space only for beta testers ;).')}
        return render(request, 'inbox/inbox.html', {'data': data})

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST or None)
            user = request.user
            if form.is_valid():
                to = request.POST['to']
                conv = request.POST['conversation']
                obj = form.save(commit=False)
                obj.user = user
                obj.to = User.objects.get(id=to)
                if conv == '0':
                    obj.conversation = get_random_string(64)
                else:
                    obj.conversation = conv
                # implementing mechanism for encrypting messages

                obj.save()

                # implementing notification system
                self.n.addNotif(user, obj.to, obj.id, obj.title)

            return redirect('/inbox')
