from django import forms
from django.forms import ModelForm
from .models import Profile, Trip, Post
from django_countries.widgets import CountrySelectWidget
from django.utils.translation import  gettext as _


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['country', 'birthday', 'cover', 'pic']
        widgets = {'country': CountrySelectWidget}


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['trip', 'profile_id', 'text']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text)>0:
            return text
        else:
            return forms.ValidationError('Error')


    def clean_trip(self):
        pass

    def clean_profile_id(self):
        pass

class TripForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.order_fields(['title', 'description', 'basePlace', 'mountainName', 'startDate', 'endDate', 'cover'])

    class Meta:
        model = Trip
        fields = {'title', 'description', 'basePlace', 'mountainName', 'startDate', 'endDate', 'cover'}
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'basePlace': _('Base place'),
            'mountainName': _('Mountain name'),
            'startDate': _('Start date'),
            'endDate': _('End date'),
            'cover': _('Cover photo')

        }
        widgets = {
            'description': forms.Textarea(),
            'startDate': forms.DateInput(attrs={'type': 'date'}),
            'endDate': forms.DateInput(attrs={'type': 'date'}),
        }


class SearchForm(ModelForm):
    searchQuery = forms.CharField(max_length=40, required=False)