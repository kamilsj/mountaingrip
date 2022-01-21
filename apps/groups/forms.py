from django import forms
from .models import Group, Thread, ThreadPost, ThreadPic
from django.utils.translation import gettext as _
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput



class PostForm(forms.ModelForm):
    class Meta:
        model = ThreadPost
        fields = ['thread', 'group', 'text', 'pic']
        widgets = {
            'pic': ClearableFileInput(attrs={'multiple': True}),
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 4096:
            return text
        else:
            raise ValidationError(_('Your post is a little bit too long.'))

    def clean_group(self):
        group = self.cleaned_data['group']
        if group.id > 0:
            if Group.objects.filter(id=group.id).exists():
                return Group.objects.get(id=group.id)
            else:
                raise ValidationError(_('Cannot add post to this group.'))
        else:
            raise ValidationError(_('There is a problem with this group'))

    def clean_thread(self):
        thread = self.cleaned_data['thread']
        if thread.id > 0:
            if Thread.objects.filter(id=thread.id).exists():
                return Thread.objects.get(id=thread.id)
            else:
                raise ValidationError(_('Cannot add post to this thread.'))
        else:
            raise ValidationError(_('There is a problem with this thread'))


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'pic', 'private']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        desc = cleaned_data.get('description')
        time_threshold = datetime.now() - timedelta(seconds=70*60)
        print(name, desc, time_threshold)
        if Group.objects.filter(name=name, description=desc, added_at__gte=time_threshold).exists():
            raise ValidationError(_('This group was added just few minutes ago.'), code='group_already_exists')


    def clean_name(self):
        name = self.cleaned_data['name']
        if 1 < len(name) < 256:
            return name
        else:
            raise ValidationError(_('Groups has to have a name :)'), code='name_too_short')

    def clean_description(self):
        desc = self.cleaned_data['description']
        if len(desc) < 1024:
            return desc
        else:
            raise ValidationError(_('Your description is a little bit too long.'), code='description_too_long')

    def clean_pic(self):
        if self.cleaned_data['pic']:
            return True
        else:
            return False


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['group', 'name', 'description']

    def clean_group(self):
        group = self.cleaned_data['group']
        if group.id > 0:
            if Group.objects.filter(id=group.id).exists:
                return group
            else:
                raise ValidationError(_('Group does not exists.'), code='group_does_not_exist')
        else:
            raise ValidationError(_('Invalid group code'), code='invalid_group')

    def clean_name(self):
        name = self.cleaned_data['name']
        if 1 < len(name) < 296:
            return name
        else:
            raise ValidationError(_('Groups has to have a name :)'), code='name_too_long')

    def clean_description(self):
        desc = self.cleaned_data['description']
        if len(desc) < 4096:
            return desc
        else:
            raise ValidationError(_('Your description is a little bit too long.'), code='description_too_long')
