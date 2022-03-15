import re
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _

from func.notif import Notif
from django.db.models import Q, Subquery

from .forms import MessageForm
from .models import Message, Attachment


class DeletedView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class SentView(View):
    def get(self, request):
        if request.user.is_authenticated:
            data = {}
            user = request.user
            if settings.BETA is True and request.session['beta'] is True:
                if Message.objects.filter(user=user, deleted=False).count() > 0:
                    sent = Message.objects.filter(user=user, deleted=False).order_by('-id').all()[:50]
                    data = {
                        'no_reply': 1,
                        'sent': sent
                    }
                else:
                    data = {'nonew:': _('No sent messages')}
            return render(request, 'inbox/sent.html', {'data': data})
        else:
            return redirect('/')

    def post(self, request):
        pass


class MessageView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            data = {}
            if id > 0:
                if settings.BETA is True and request.session['beta'] is True:
                    if Message.objects.filter(Q(id=id) & (Q(user=request.user) | Q(to=request.user))).exists():
                        message = Message.objects.get(id=id)
                        if message.to.id == request.user.id:
                            message.read = True
                            message.save()
                        conv = message.conversation
                        messages = Message.objects.filter(conversation=conv, deleted=False).exclude(id=id).order_by('-id').all()[:50]
                        photos = Attachment.objects.filter(message__in=Subquery(Message.objects.filter(conversation=conv, deleted=False, attachments=True).values('id').order_by('-id'))).all()
                        if messages.count() > 0:
                            data = {
                                'photos': photos,
                                'message': message,
                                'messages': messages
                            }
                        else:
                            data = {
                                'photos': photos,
                                'message': message
                            }
                    else:
                        return redirect('/inbox/')
            return render(request, 'inbox/message.html', {'data': data})
        else:
            return redirect('/')

    def post(self, request, id):
        if request.method == 'POST':
            try:
                message = Message.objects.get(id=id)
                user = message.user
                if message.title[0] != '+':
                    title = '+' + message.title
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
                    if request.FILES:
                        photos = request.FILES.getlist('pic')
                        if len(photos) < 30:
                            for photo in photos:
                                Attachment.objects.create(user=user, message=obj, pic=photo)
                            Message.objects.filter(pk=obj.id).update(attachments=True) 
                        else:
                            raise ValidationError(_('You can not send more than 30 photos'))     
                    return redirect('/inbox/message/' + str(obj.id))
            except Message.DoesNotExist:
                pass


class Inbox(View):
    form_class = MessageForm
    n = Notif(1)

    def get(self, request):
        if request.user.is_authenticated:
            data = {}
            if settings.BETA is True and request.session['beta'] is True:
                count = Message.objects.filter(to=request.user, deleted=False).count()
                if count > 0:
                    # messages = Message.objects.filter(to=request.user).order_by('-id').all()[:50]
                    messages = Message.objects.filter(deleted=False, id__in=Subquery(
                        Message.objects.filter(to=request.user).order_by('conversation', '-id').distinct('conversation').
                            values('id'))).order_by('-id').all()
                    data = {
                        'messages': messages,
                    }
                else:
                    data = {'nonew': _('No messages')}
            else:
                data = {'info': _('You cannot be here. Space only for beta testers ;).')}
            return render(request, 'inbox/inbox.html', {'data': data})
        else:
            return redirect('/')
                        
    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST or None, request.FILES or None)
            user = request.user
            if form.is_valid():
                to = request.POST['to']
                conv = request.POST['conversation']
                obj = form.save(commit=False)
                obj.user = user
                obj.deleted = False
                obj.read = False
                obj.to = User.objects.get(id=to)
                if conv == '0':
                    obj.conversation = get_random_string(64)
                else:
                    obj.conversation = conv
                # implementing mechanism for encrypting messages
                
                obj.save()
                
                if request.FILES:
                    photos = request.FILES.getlist('pic')
                    if len(photos) < 30:
                        for photo in photos:
                            Attachment.objects.create(user=user, message=obj, pic=photo)
                        Message.objects.filter(pk=obj.id).update(attachments=True)
                    else:
                        raise ValidationError(_('You can upload maximum 30 photos at once'))

                # implementing notification system
                self.n.addNotif(user, obj.to, obj.id, obj.title)

            return redirect('/inbox/message/'+str(obj.id)+'/')
