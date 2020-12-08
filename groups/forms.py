from django import forms
from django.forms import ModelForm
from .models import Group, GroupPost
from django.utils.translation import gettext as _


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
        return self.cleaned_data['description']

