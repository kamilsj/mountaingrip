from django import forms
from django.forms import ModelForm
from .models import Message
from django.utils.translation import gettext as _


class MessageForm(forms.ModelForm):
    pic = forms.ImageField(required=False)

    class Meta:
        model = Message
        fields = ['to', 'text', 'title', 'pic']
        widgets = {
            'pic': forms.ClearableFileInput(attrs={'required': False, 'multiple': True})
        }
