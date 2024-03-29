from apps.desire.models import Desire, DesireSearch
from start.models import Trip, Profile
from django.contrib.auth.models import User
from django.db.models import Q

from django.utils.translation import gettext as _


class DesireClass:

    def __init__(self, how, what, desire, user):
        self.how = int(how)  
        self.what = int(what)
        self.desire = str(desire)
        self.user = user

    def ParseHow(self):
        if self.how == 1:
            return _('wants')
        else:
            return ''          

    def ParseWhat(self):
        if self.what == 1:
            return _('to meet')
        elif self.what == 2:
            return _('to hike')
        elif self.what == 3:
            return _('to climb')
        elif self.what == 4:
            return _('to ski from')
        elif self.what == 5:
            return _('to visit')
        else:
            return ''

    def SearchResults(self):
        if len(self.desire) > 1:
            proxy = Desire.objects.filter(desire=self.desire).exclude(user=self.user)
            if proxy.count() == 1:
                des_id = proxy.get()
                data = DesireSearch.objects.filter(id=des_id.id).exclude(user=self.user).order_by('-id').all()
            else:
                data = ''
        return data

    def TripData(self):
        if self.what > 1:
            data = Trip.objects.filter(Q(mountainName__icontains=self.desire) | Q(basePlace__icontains=self.desire)).order_by('-id').all()            
        else:
            data = ''
        return data

    def UserData(self):
        if self.what == 1:
            data = User.objects.filter(Q(username__icontains=self.desire) | Q(first_name__icontains=self.desire) | Q(last_name__icontains=self.desire)).order_by('-id').all()
        else:
            data = ''
        return data 