from django import forms
from .models import EJP
from django.utils.translation import gettext as _


class EJPForm(forms.ModelForm):
    class Meta:
        model = EJP
        fields = ['date', 'n1', 'n2', 'n3', 'n4', 'n5', 'p1', 'p2']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


