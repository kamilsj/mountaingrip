from django import forms
from .models import HealthData
from django.utils.translation import gettext as _

class HealthDataForm(forms.ModelForm):
    class Meta:
        model = HealthData
        fields = ['weight', 'neck', 'waist', 'hip']