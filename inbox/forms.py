from django import forms
from django.forms import ModelForm
from .models import Message


from django.utils.translation import gettext as _


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = []
