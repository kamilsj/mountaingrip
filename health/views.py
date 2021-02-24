from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta
from django.views import View
from .forms import HealthDataForm
from .models import HealthData
from start.models import Profile
from func.modules.importer import ImportStravaDataApi
from func.modules.services.strava import *

class Index(View):
    form_class = HealthDataForm

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            data = {
                'date': datetime.today()
            }
            if not HealthData.objects.filter(user=user.id).filter(date__startswith=date.today()).exists():
                form = self.form_class
                data['added'] = 1
            else:
                form = {}
                data['added'] = 0
        else:
            form = {}
            data = {}

        return render(request, 'health/index.html', {'form': form, 'data': data})

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            form = self.form_class(request.POST)
            if form.is_valid():
                user_profile = Profile.objects.get(user=user.id)
                if user_profile.height > 0 and user_profile.height <= 250:
                    bmi = form.cleaned_data['weight'] / (user_profile.height / 100) ** 2  # FORMULA FOR BMI
                else:
                    bmi = 0
                obj = form.save(commit=False)
                obj.bmi = bmi
                obj.user = user
                obj.save()

        return redirect('/health/')


class ImportActivities(View):

    def get(self, request):
        data = {}
        strava = 0
        strava_url = ''
        code = request.GET.get('code')
        if code:
            strava = StravaToken(code=code)
        else:
            strava_url = StravaUrl()

        if strava and strava != 0:
            athlete = strava.get_athlete()
            activities = strava.get_activities()
            imported = ImportStravaDataApi()
            imported.AddApi(request.user, activities)

            data = {
                'athlete': athlete.firstname,

            }

        return render(request, 'health/import_activities.html', {
            'data': data,
            'strava_url': strava_url
        })

    def post(self, request):
        pass


class Analytics(View):

    def get(self, request):
        from bokeh.io import output_notebook
        data = {}

        return render(request, 'health/activities.html', {'data': data})


    def post(self, request):
        pass


