from django import forms
from django.forms import ModelForm
from .models import Profile, Trip
from django_countries.widgets import CountrySelectWidget
from django.utils.translation import  gettext as _


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['country', 'coverId', 'picId']
        widgets = {'country': CountrySelectWidget}


class TripForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.order_fields(['title', 'description', 'basePlace', 'mountainName', 'startDate', 'endDate', 'coverId'])

    class Meta:
        model = Trip
        fields = {'title', 'description', 'basePlace', 'mountainName', 'startDate', 'endDate', 'coverId'}
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'basePlace': _('Base place'),
            'mountainName': _('Mountian name'),
            'startDate': _('Start date'),
            'endDate': _('End date'),
            'coverId': _('Cover photo')

        }
        widgets = {
            'description': forms.Textarea(),
            'startDate': forms.DateInput(attrs={'type': 'date'}),
            'endDate': forms.DateInput(attrs={'type': 'date'}),
        }


class SearchForm(ModelForm):
    searchQuery = forms.CharField(max_length=40, required=False)