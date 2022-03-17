from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Profile, Trip, Post
from django_countries.widgets import CountrySelectWidget
from django.utils.translation import gettext as _


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pic', 'cover', 'birthday', 'gender', 'country', 'height']
        labels = {
            'pic': _('Your profile photo'),
            'cover': _('Your cover photo'),
            'birthday': _('Birthday'),
            'gender': _('Gender'),
            'country': _('Country'),
            'height': _('Height')
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'country': CountrySelectWidget(),
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['trip', 'profile_id', 'text']

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) > 1 and len(text) < 4096:
            return text
        elif len(text) > 4096:
            raise ValidationError(_('Your post is too long.'))
        else:
            raise ValidationError(_('You have to write something :)'))

    def clean_trip(self):
        trip = self.cleaned_data['trip']
        if trip.id > 0:
            return trip

    def clean_profile_id(self):
        profile_id = self.cleaned_data['profile_id']
        if profile_id > 0:
            return profile_id
        else:
            return 0


class TripForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.order_fields(['title', 'description', 'basePlace', 'mountainName', 'startDate', 'endDate', 'cover', 'private'])

    class Meta:
        model = Trip
        fields = {'title', 'description', 'basePlace', 'mountainName', 'startDate', 'endDate', 'cover', 'private'}
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


    
    def clean_dates(self):
        start_date = self.cleaned_data['startDate']
        end_date = self.cleaned_data['endDate']
        if end_date < start_date:
            raise ValidationError(_('Something is wrong'))


class SearchForm(ModelForm):
    searchQuery = forms.CharField(max_length=40, required=False)