from errno import ESTALE
from http.client import FORBIDDEN
from django.shortcuts import render, redirect
from django.views import View
from .forms import GroupForm, ThreadForm, PostForm
from .models import Group, Thread, ThreadPost, PrivateGroup, FollowedGroup, FollowedThread, ThreadPic

from django.db.models import Q, Subquery
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import datetime
from func.notif import Notif


class GroupExplore(View):

    def get(self, request):
        data = {}

        groups = Group.objects.filter(private=False).order_by('-added_at').all()[:20]
        yours = Group.objects.filter(user=request.user).order_by('-added_at').all()[:20]
        private = Group.objects.filter(private=True, id__in=Subquery(
            PrivateGroup.objects.filter(user=request.user).distinct('group_id').values('group_id'))).order_by('-id').all()[:20]
        followed = Group.objects.filter(id__in=Subquery(
            FollowedGroup.objects.filter(user=request.user).distinct('group_id').values('group_id'))).order_by('-id').all()[:20]

        data = {
            'followed': followed,
            'groups': groups,
            'yours': yours,
            'private': private
        }

        return render(request, 'groups/index.html', {'data': data})

    def post(self, request):
        pass


class GroupViewSettings(View):
    def get(self, request, id=0):
        data = {}
        if id > 0:
            return render(request, 'groups/settings.html', {'data': data})
        else:
            return redirect('/groups/')


    def post(self, request, id=0):
        pass


class GroupView(View):
    form_class = ThreadForm
    time_threshold = datetime.datetime.now() - datetime.timedelta(minutes=70)
    data = {}

    def get(self, request, id=0):
        user = request.user
        if user.is_authenticated:
            if id > 0:
                if Group.objects.filter(id=id).exists():
                    group = Group.objects.get(id=id)
                    if group.user == request.user:
                        is_admin = True
                    else:
                        is_admin = False
                    if FollowedGroup.objects.filter(user=user, group=group).exists():
                        group_followed = True
                    else:
                        group_followed = False 
                          
                    if group.private:
                        if PrivateGroup.objects.filter(user=request.user,
                                                    group=group).exists() or request.user == group.user:
                            threads = Thread.objects.filter(group=group).order_by('-added_at').all()[:20]
                            self.data = {
                                'is_admin': is_admin,
                                'group': group,
                                'threads': threads,
                                'group_followed': group_followed
                            }
                        else:
                            self.data = {
                                'private': 1
                            }

                    else:
                        threads = Thread.objects.filter(group=group).order_by('-added_at').all()[:20]
                        self.data = {
                            'is_admin': is_admin,
                            'group': group,
                            'threads': threads,
                            'group_followed': group_followed
                        }
                else:
                    self.data = {
                        'nogroup': 1,
                    }
            else:
                return redirect('/groups/')
        else:
            return redirect('/') 

        return render(request, 'groups/view.html', {'data': self.data, 'form': self.form_class})

    def post(self, request, id=0):
        user = request.user
        form = self.form_class(request.POST or None)
        if request.method == 'POST' and user.is_authenticated:
            if form.is_valid():
                group = form.clean_group()
                name = form.clean_name()
                desc = form.clean_description()
                if not Thread.objects.filter(user=user, group=group, name=name,
                                             added_at__lt=self.time_threshold).exists():
                    n = Thread.objects.create(
                        user=user,
                        group=group,
                        name=name,
                    )
                    if n.id:
                        thread = Thread.objects.get(id=n.id)
                        if not ThreadPost.objects.filter(user=user, group=group, thread=thread, text=desc).exists():
                            if ThreadPost.objects.create(
                                    user=user,
                                    group=group,
                                    thread=thread,
                                    text=desc
                            ):
                                return redirect('/groups/' + str(group.id) + '/' + str(n.id) + '/')
                        else:
                            return redirect('/groups/' + str(group.id) + '/' + str(n.id) + '/')
                else:
                    return redirect('/groups/' + str(group.id) + '/')

            return render(request, 'groups/view.html', {'data': self.data, 'form': form})


class ThreadView(View):
    form_class = PostForm
    data = {}
    time_threshold = datetime.datetime.now() - datetime.timedelta(minutes=70)

    def get(self, request, gid=0, tid=0):
        user = request.user
        page = 20
        followed = False
        if gid > 0 and tid > 0:
            thread = Thread.objects.get(id=tid)
            group = Group.objects.get(id=gid)
            if ThreadPost.objects.filter(thread=thread, group=group).count() > 0:
                posts = ThreadPost.objects.filter(thread=thread, group=group).order_by('added_at').all()[:page]
                pics = ThreadPic.objects.filter(thread=thread, group=group).order_by('added_at').all()
                if FollowedThread.objects.filter(user=user, thread=thread).exists():
                    followed = True
            
                self.data = {
                    'user': user,
                    'followed': followed,
                    'thread': thread,
                    'pics': pics,
                    'posts': posts,

                }
            else:
                self.data = {
                    'noposts': 1
                }

            return render(request, 'groups/thread.html', {'data': self.data, 'from': self.form_class})

    def post(self, request, gid=0, tid=0):
        user = request.user
        self.data = {
            'user': user,
        }
        form = self.form_class(request.POST or None, request.FILES or None)
        if request.method == 'POST' and user.is_authenticated:
            if form.is_valid():
                print('OK')
                if gid > 0 and tid > 0:
                    text = form.clean_text()
                    group = form.clean_group()
                    thread = form.clean_thread()
                    
                    if not ThreadPost.objects.filter(group=group, thread=thread, text=text,
                                                     added_at__lte=self.time_threshold).exists():
                        post = ThreadPost.objects.create(user=user, group=group, thread=thread, text=text, attachments=False)
                        if request.FILES:                            
                            photos = request.FILES.getlist('pic')
                            if len(photos) < 30:
                                for photo in photos:
                                    ThreadPic.objects.create(user=user, group=group, thread=thread, post=post, pic=photo)
                                ThreadPost.objects.filter(id=post.id).update(attachments=True)
                            else:
                                raise ValidationError(_('You can upload a maximum of 30 photos per post.'))

                        return redirect('/groups/' + str(group.id) + '/' + str(thread.id) + '/')

                    else:
                        raise ValidationError(_('This post was just added'))
                else:
                    raise ValidationError(_('There is another serious problem'))

            return render(request, 'groups/thread.html', {'data': self.data, 'from': form})


class GroupCreate(View):
    form_class = GroupForm

    def get(self, request):
        return render(request, 'groups/create.html', {'form': self.form_class})

    def post(self, request):
        if request.method == 'POST' and request.user.is_authenticated:
            form = self.form_class(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.clean()
                name = form.clean_name()
                desc = form.clean_description()
                form.name = name
                form.description = desc
                n = form.save(commit=False)
                if form.clean_pic():
                    n.pic = request.FILES['pic']
                else:
                    n.pic = None
                n.user = request.user
                n.save()
                if n.id:
                    return redirect('/groups/' + str(n.id) + '/')

            return render(request, 'groups/create.html', {'form': form})
