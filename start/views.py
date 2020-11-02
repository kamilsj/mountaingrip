from django.shortcuts import redirect, render
from django.utils import translation
from django.contrib.auth.models import User
from django.utils.translation import  gettext as _
from django.views import View

from .models import Trip, Profile, Post, Comment
from .forms import TripForm, SearchForm, PostForm

from func.site_functions import common

import datetime
from django.utils import timezone

import googlemaps
from django.conf import settings
gkey = settings.GKEY
gmaps = googlemaps.Client(key=gkey)

def index(request):

    if request.user.is_authenticated:
        user = request.user
        date = datetime.datetime.now(tz=timezone.utc)

        data = {}
        addedby = {}

        '''
        Trips added within last 2 weeks
        if there are not any ... show at least last 10
        Which are not yet finished
        '''
        from_date = date - datetime.timedelta(days=14)
        if Trip.objects.filter(added_at__range=[from_date, date]).count() > 0:
            trips = Trip.objects.filter(added_at__range=[from_date, date]).all()[:15]
        else:
            trips = Trip.objects.all()[:15]

        data = {
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
                if Profile.objects.filter(user_id=id).exists():
                    profile = Profile.objects.get(user_id=id)
                    pic = common.check_pic(profile.cover.url)
                    cover = common.check_cover(profile.pic.url)
                    data = {
                        'name': name,
                        'curl': cover,
                        'purl': pic
                    }
        except User.DoesNotExist:
            data = {
                'notexists': 1,
                'name': _('User does not exist')
            }
    else:

        user = request.user
        if Profile.objects.filter(user_id=user.id).exists():
            name = user.get_full_name()
            profile = Profile.objects.get(user_id=user.id)
            if profile.cover:
                cover = profile.cover.url
            else:
                cover = 'https://mountiangrip.s3.amazonaws.com/media/profile/P1000193_B55pk0B.jpg'

            if profile.pic:
                pic = profile.pic.url
            else:
                pic = 'https://mountiangrip.s3.amazonaws.com/assets/defaultProfilePicture.jpg'

            data = {
                'name': name,
                'curl': cover,
                'purl': pic
            }
        else:
            data = {
                'notexists': 1,
                'name': _('User does not exist')
            }
    return render(request, 'profile.html', {'data': data})


class ProfileUpdate(View):
    form = Profile
    template_name = 'start/profile_update.html'

    def get(self, request):
        pass

    def post(self, request, id=0):
        pass


def explore(reqest):
    data = {}
    return render(reqest, 'start/explore.html', {'data': data})


def trip(request, id=0):

    data = {}
    location_m_name = {}
    location_b_place = {}
    if id and id != 0:
        if Trip.objects.filter(id=id).exists():
            trip = Trip.objects.get(id=id)
            if trip:
                if Post.objects.filter(trip_id=id).count()>0:
                    posts = Post.objects.filter(trip_id=id).all()
                    if Comment.objects.filter(trip_id=id).count()>0:
                        pass

                b_place = gmaps.geocode(trip.basePlace)
                m_name = gmaps.geocode(trip.mountainName)

                location_b_place = {
                    'name': b_place[0]['formatted_address'],
                    'lat': b_place[0]['geometry']['location']['lat'],
                    'lng': b_place[0]['geometry']['location']['lng']
                }
                location_m_name = {
                    'name': m_name[0]['formatted_address'],
                    'lat': m_name[0]['geometry']['location']['lat'],
                    'lng': m_name[0]['geometry']['location']['lng']
                }

                data = {
                    'id': trip.id,
                    'gmaps_key': gkey,
                    'basePlace': location_b_place,
                    'mountainName': location_m_name,
                    'url': trip.cover.url,
                    'title': trip.title,
                    'description': trip.description,
                    'startDate': trip.startDate,
                    'endDate': trip.endDate
                }

            else:
                data = {'notrip': 1}
        else:
            data = {'notrip': 1}

    else:
        data = {'notrip': 1}

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
        if request.method == 'POST' and request.user.is_authenticated:
            user = request.user
            form = self.form_class(request.POST, request.FILES)

            if form.is_valid():
                #check if form was already added
                #TODO request files of particular size and order
                obj = form.save(commit=False)
                obj.user = user
                if not Trip.objects.filter(title=obj.title, user=user, endDate=obj.endDate, startDate=obj.startDate).exists():


                    obj.save()
                    return redirect('/start/trip/' + str(obj.id))
                else:
                    return redirect('/start/trip/')


def addpost(requst):
    if requst.method == 'POST' and requst.user.is_authenticated:
        user = requst.user
        form = PostForm(requst.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            if not Post.object.filter(text=obj.text, user=obj.user).exists():
                obj.save()
                return redirect('/start/trip/'+str(requst.POST['trip_id']))
            else:
                return redirect('/start/trip/')

def addfriend(request):
    pass