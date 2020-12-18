from django import forms
from .models import Group, Thread, ThreadPost, ThreadPic
from django.utils.translation import gettext as _


class PostForm(forms.ModelForm):
    class Meta:
        model = ThreadPost
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 4096:
            return text
        else:
            raise forms.ValidationError(_('Your description is a little bit too long.'))

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'pic']

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 1 and len(name) < 296:
            return name
        else:
            raise forms.ValidationError(_('Groups has to have a name :)'))

    def clean_description(self):
        desc = self.cleaned_data['description']
        if len(desc)<1024:
            return desc
        else:
            raise forms.ValidationError(_('Your description is a little bit too long.'))

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
        if group.id>0:
            if Group.objects.filter(id=group.id).exists:
                return group
            else:
                raise forms.ValidationError(_('Group does not exists.'))
        else:
            raise forms.ValidationError(_('Invalid groud code'))


    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 1 and len(name) < 296:
            return name
        else:
            raise forms.ValidationError(_('Groups has to have a name :)'))

    def clean_description(self):
        desc = self.cleaned_data['description']
        if len(desc) < 4096:
            return desc
        else:
            raise forms.ValidationError(_('Your description is a little bit too long.'))