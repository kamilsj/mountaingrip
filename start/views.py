from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.views import View
from django.contrib.auth.decorators import login_required

from .models import Trip, Profile, Post, Comment, TripJoined
from .forms import TripForm, SearchForm, PostForm, ProfileForm

from func.site_functions import common

import datetime
from django.utils import timezone

import googlemaps
from django.conf import settings
gkey = settings.GKEY
gmaps = googlemaps.Client(key=gkey)


def tensorflow():
    pass


def index(request):
    if request.user.is_authenticated:
        user = request.user
        date = datetime.datetime.now(tz=timezone.utc)

        data = {}
        addedby = {}
        posts = {}
        '''
        Trips added within last 2 weeks
        if there are not any ... show at least last 10
        Which are not yet finished
        '''
        from_date = date - datetime.timedelta(days=14)
        if Trip.objects.filter(added_at__range=[from_date, date]).count() > 15:
            trips = Trip.objects.filter(added_at__range=[from_date, date]).all()[:16]
        else:
            trips = Trip.objects.all()[:16]

        data = {
            'user': user.get_full_name(),
            'trips': trips,
            'posts': posts,
        }

        return render(request, 'mountiangrip.html', {'data': data})

    else:
        return redirect('/')


class ProfileView(View):

    def get(self, request, id=0):
        form = PostForm()
        data = {}
        if id and id != 0:
            try:
                user = User.objects.get(id=id)
                if user:
                    name = user.get_full_name()
                    if Profile.objects.filter(user_id=id).exists():
                        profile = Profile.objects.get(user_id=id)
                        pic = common.check_pic(profile.pic)
                        cover = common.check_cover(profile.cover)
                        if Post.objects.filter(profile_id=id).count() > 0:
                            posts = Post.objects.filter(profile_id=id).order_by('-added_at').all()
                        else:
                            posts = ''
                        data = {
                            'id': id,
                            'name': name,
                            'curl': cover,
                            'purl': pic,
                            'posts': posts
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
                pic = common.check_pic(profile.pic)
                cover = common.check_cover(profile.cover)
                if Post.objects.filter(profile_id=user.id).count() > 0:
                    posts = Post.objects.filter(profile_id=user.id).order_by('-added_at').all()
                else:
                    posts = ''

                data = {
                    'id': user.id,
                    'name': name,
                    'curl': cover,
                    'purl': pic,
                    'posts': posts
                }

            else:
                data = {
                    'notexists': 1,
                    'name': _('User does not exist')
                }
        return render(request, 'profile.html', {'data': data, 'form': form})


    def post(self, request, id=0):
        form = PostForm(request.POST)
        user = request.user
        if request.method == 'POST' and user.is_authenticated:
            if form.is_valid():
                text = form.clean_text()
                profile_id = form.clean_profile_id()
                if Post.objects.create(
                        user=user,
                        profile_id=profile_id,
                        text=text
                ):
                    return redirect('/start/profile/' + str(profile_id) + '/')
            else:
                return redirect('/start/profile/')

class ProfileUpdate(View):
    form_class = ProfileForm
    template_name = 'start/profile_update.html'

    def get(self, request):
        init_data = Profile.objects.get(user=request.user)
        form = self.form_class(initial={'pic': init_data.pic, 'cover': init_data.cover, 'birthday': init_data.birthday,
                                        'gender': init_data.gender, 'country': init_data.country, 'height': init_data.height})
        return render(request, 'start/profile_update.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            form = self.form_class(request.POST or None, request.FILES or None)
            if form.is_valid():
                if Profile.objects.filter(user=user).exists():
                    profile = Profile.objects.get(user=user)
                    if not form.cleaned_data.get('pic'):
                        pic = profile.pic
                    else:
                        pic = form.cleaned_data.get('pic').url
                    if not form.cleaned_data.get('cover'):
                        cover = profile.cover
                    else:
                        cover = form.cleaned_data.get('cover')

                    Profile.objects.filter(user=user).update(
                        pic=pic,
                        cover=cover,
                        gender=form.cleaned_data.get('gender'),
                        birthday=form.cleaned_data.get('birthday'),
                        country=form.cleaned_data.get('country'),
                    )
                    return redirect('/start/profile/')
                else:
                    pass
            else:
                return render(request, 'start/profile_update.html', {'form': form})


class Explore(View):

    def get(self,request):
        data = {}
        return render(request, 'start/explore.html', {'data': data})

    def post(self, request):
        pass


class TripView(View):

    def get(self, request, id=0):
        data = {}
        location_m_name = {}
        location_b_place = {}
        comments = ''
        posts = ''
        user = request.user
        if id and id != 0:
            if Trip.objects.filter(id=id).exists():
                trip = Trip.objects.get(id=id)
                if trip:
                    joined = TripJoined.objects.filter(trip=trip).count()
                    if Post.objects.filter(trip_id=id).count() > 0:
                        posts = Post.objects.filter(trip_id=id).order_by('-added_at').all()
                        if Comment.objects.filter(trip_id=id).count() > 0:
                            comments = ''


                    if trip.blat == 0 and trip.blng == 0 and trip.mlat == 0 and trip.mlng == 0:

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

                        Trip.objects.filter(id=id).update(
                            blat=b_place[0]['geometry']['location']['lat'],
                            blng=b_place[0]['geometry']['location']['lng'],
                            mlat=m_name[0]['geometry']['location']['lat'],
                            mlng=m_name[0]['geometry']['location']['lng']
                        )
                    else:
                        location_b_place = {
                            'name': trip.basePlace,
                            'lat': trip.blat,
                            'lng': trip.blng
                        }
                        location_m_name = {
                            'name': trip.mountainName,
                            'lat': trip.mlat,
                            'lng': trip.mlng
                        }

                    data = {
                        'id': trip.id,
                        'posts': posts,
                        'comments': comments,
                        'joined': joined,
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
            return redirect('/start/trip/explore/')

        return render(request, 'start/trip.html', {'data': data})


    def post(self, request, id=0):
        form = PostForm(request.POST)
        if request.method == 'POST' and request.user.is_authenticated:
            if form.is_valid():
                trip = form.clean_trip()
                text = form.clean_text()
                profile_id = form.clean_profile_id()
                user = request.user
                if Post.objects.create(
                    user=user,
                    profile_id=profile_id,
                    trip=trip,
                    text=text
                ):
                        return redirect('/start/trip/'+str(trip.id)+'/')
            else:
                return HttpResponse(form.errors)

        else:
            return HttpResponse('nothing')


def q(request):
    groups = {}
    trips = {}
    profile = {}
    posts = {}
    data = {}

    if request.method == 'GET':
        q = request.GET['what']
        #finding stuff and memorizing search query
        


        
        return render(request, 'searchresult.html', {'data': data, 'q': q})
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

