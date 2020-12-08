from django.shortcuts import render, redirect
from django.views import View
from .forms import GroupForm, GroupPost
from .models import Group
from django.utils.translation import gettext as _



class GroupExplore(View):

    def get(self, request):
        data = {}

        groups = Group.objects.all()[:17]
        data = {
            'groups': groups,
        }


        return render(request, 'groups/index.html', {'data': data})

    def post(self, request):
        pass


class GroupView(View):
    form_class = GroupPost

    def get(self, request, id=0):
        data = {}

        if id > 0:
            if Group.objects.filter(id=id).exists():
                group = Group.objects.get(id=id)


        else:
            return redirect('/groups/')

        return render(request, 'groups/view.html', {'data': data, 'form': self.form_class})

    def post(self, request):
        pass


class GroupCreate(View):
    form_class = GroupForm

    def get(self, request):
        data = {}
        return render(request, 'groups/create.html', {'form': self.form_class})

    def post(self, request):
        user = request.user
        if request.method == 'POST' and user.is_authenticated:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                name = form.clean_name()
                desc = form.clean_description()
                n = Group(user=user, name=name, description=desc, pic=request.FILES['pic'])
                if n.save():
                    return redirect('/groups/'+str(n.id)+'/')

            else:
                return render(request, 'groups/create.html', {'form': form})


