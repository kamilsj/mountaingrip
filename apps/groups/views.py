from django.shortcuts import render, redirect
from django.views import View
from .forms import GroupForm, ThreadForm, PostForm
from .models import Group, Thread, ThreadPost
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import datetime
from func.notif import Notif



class GroupExplore(View):

    def get(self, request):
        data = {}

        groups = Group.objects.filter(private=False).order_by('-added_at').all()[:20]
        yours = Group.objects.filter(user=request.user).order_by('-added_at').all()[:20]
        data = {
            'groups': groups,
            'yours': yours
        }

        return render(request, 'groups/index.html', {'data': data})

    def post(self, request):
        pass


class GroupView(View):
    form_class = ThreadForm
    time_threshold = datetime.datetime.now() - datetime.timedelta(minutes=70)
    data = {}

    def get(self, request, id=0):
        if id > 0:
            if Group.objects.filter(id=id).exists():
                group = Group.objects.get(id=id)
                threads = Thread.objects.filter(group=group).order_by('-added_at').all()[:20]
                self.data = {
                    'group': group,
                    'threads': threads
                }
            else:
                self.data = {
                    'nogroup': 1,
                }
        else:
            return redirect('/groups/')

        return render(request, 'groups/view.html', {'data': self.data, 'form': self.form_class})

    def post(self, request, id=0):
        user = request.user
        form = self.form_class(request.POST or None)
        if request.method == 'POST' and user.is_authenticated:
            if form.is_valid():
                group = form.clean_group()
                name = form.clean_name()
                desc = form.clean_description()
                if not Thread.objects.filter(user=user, group=group, name=name, added_at__lt=self.time_threshold).exists():
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
                                return redirect('/groups/'+str(group.id)+'/'+str(n.id)+'/')
                        else:
                            return redirect('/groups/'+str(group.id)+'/'+str(n.id)+'/')
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
        if gid > 0 and tid > 0:
            thread = Thread.objects.get(id=tid)
            group = Group.objects.get(id=gid)
            if ThreadPost.objects.filter(thread=thread, group=group).count() > 0:
                posts = ThreadPost.objects.filter(thread=thread, group=group).all()[:page]
                self.data = {
                    'user': user,
                    'thread': thread,
                    'posts': posts,
                }

            return render(request, 'groups/thread.html', {'data': self.data, 'from': self.form_class})

    def post(self, request, gid=0, tid=0):
         user = request.user
         form = self.form_class(request.POST or None)
         if request.method == 'POST' and user.is_authenticated:
            if form.is_valid():
                if gid > 0 and tid > 0:
                    text = form.clean_text()
                    group = form.clean_group()
                    thread = form.clean_thread()

                    if not ThreadPost.objects.filter(group=group, thread=thread, text=text, added_at__lte=self.time_threshold).exists():
                        post = ThreadPost.objects.create(user=user, group=group,  thread=thread, text=text)
                        if post:
                            return redirect('/groups/'+str(group.id)+'/'+str(thread.id)+'/')
                        else:
                            pass
                else:
                    pass

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
                    return redirect('/groups/'+str(n.id)+'/')

            return render(request, 'groups/create.html', {'form': form})


