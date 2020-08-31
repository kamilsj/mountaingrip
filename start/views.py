from django.shortcuts import redirect, render
from django.utils import translation
from django.contrib.auth.models import User
from django.utils.translation import  gettext as _
from django.views import View
from .models import Trip, Profile
from .forms import TripForm, SearchForm

import datetime

def index(request):

    if request.user.is_authenticated:
        user = request.user


        data = {}

        '''
        Trips added within last 2 weeks
        if there are not any ... show at least last 10
        Which are not yet finished
        '''
        from_date = datetime.datetime.now() - datetime.timedelta(days=14)
        if Trip.objects.filter(added_at__range=[from_date, datetime.datetime.now()]).count() > 0:
            trips = Trip.objects.filter(added_at__range=[from_date, datetime.datetime.now()]).all()[:15]
        else:
            trips = Trip.objects.all()[:15]



        data={
            'user': user.get_full_name(),
            'trips': trips
        }


        return render(request, 'mountiangrip.html', {'data': data})

    else:
        return redirect('/')


def profile(request, id=0):

    data = {}
    if id and id != 0:
        try:
            user = User.objects.get(id=id)
            if user:
                name = user.get_full_name()
                if Profile.objects.filter(userId=id).exists():
                    profile = Profile.objects.get(userId=id)
                    if profile.coverId:
                        coverid = profile.coverId.url
                    else:
                        coverid = 'https://mountiangrip.s3.amazonaws.com/media/profile/P1000193_B55pk0B.jpg'

                    if profile.picId:
                        picid = profile.picId.url
                    else:
                        picid = 'https://mountiangrip.s3.amazonaws.com/assets/defaultProfilePicture.jpg'

                    data = {
                        'name': name,
                        'curl': coverid,
                        'purl': picid
                    }
        except User.DoesNotExist:
            data = {
                'notexists': 1,
                'name': _('User does not exist')
            }
    else:

        user = request.user
        print(user)

        if Profile.objects.filter(userId=user.id).exists():
            name = user.get_full_name()
            profile = Profile.objects.get(userId=user.id)
            if profile.coverId:
                coverid = profile.coverId.url
            else:
                coverid = 'https://mountiangrip.s3.amazonaws.com/media/profile/P1000193_B55pk0B.jpg'

            if profile.picId:
                picid = profile.picId.url
            else:
                picid = 'https://mountiangrip.s3.amazonaws.com/assets/defaultProfilePicture.jpg'

            data = {
                'name': name,
                'curl': coverid,
                'purl': picid
            }
        else:
            data = {
                'notexists': 1,
                'name': _('User does not exist')
            }


    return render(request, 'profile.html', {'data': data})


def explore(reqest):
    data = {}
    return render(reqest, 'start/explore.html', {'data': data})


def trip(request, id=0):
    data = {}
    if id and id != 0:
        if Trip.objects.filter(id=id).exists():
            trip = Trip.objects.get(id=id)
            if trip:
                data = {
                    'url': trip.coverId.url,
                    'title': trip.title,
                    'description': trip.description,
                    'startDate': trip.startDate,
                    'endDate': trip.endDate
                }

            else:
                data = {
                    'notrip': 1,

                }
        else:
            data = {
                'notrip': 1,

            }

    else:

        data = {
            'notrip': 1,

        }

    return render(request, 'start/trip.html', {'data': data})


def q(request):

    if request.method == 'GET':
        q = request.GET['q']
        #finding stuff and memorizing search query



        result = ''
        return render(request, 'searchresult.html', {'result': result, 'q': q})
    else:
        return None


class AddTrip(View):
    form_class = TripForm
    template_name = 'start/addtrip.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                #check if form was already added
                #TODO request files of paricular size and order
                obj = form.save(commit=False)
                obj.userId = user.id
                if not Trip.objects.filter(title=obj.title, userId=user.id, endDate=obj.endDate, startDate=obj.startDate).exists():


                    obj.save()
                    return redirect('/start/trip/' + str(obj.id))
                else:
                    return redirect('/start/trip/')
