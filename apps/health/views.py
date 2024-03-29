from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta
from django.views import View
from .forms import HealthDataForm
from .models import HealthData, ActivitiesStravaData
from start.models import Profile
from func.modules.importer import ImportStravaDataApi
from func.modules.services.strava import *

import numpy as n
from func.AI.learn import WeightCalculations


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
                if 0 < user_profile.height <= 300:
                    bmi = form.cleaned_data['weight'] / (user_profile.height / 100) ** 2  # FORMULA FOR BMI
                else:
                    bmi = 0
                obj = form.save(commit=False)
                obj.bmi = bmi
                obj.user = user
                obj.save()

        return redirect('/health/')


class Summary(View):

    def get(self, request):
        if request.user.is_authenticated:
            from collections import OrderedDict
            data = {}
            res = {}
            i = 0
            strava = ActivitiesStravaData.objects.filter(user=request.user).values('start_date',
                                                                                'distance',
                                                                                'average_speed').order_by('-start_date')
            body = HealthData.objects.filter(user=request.user).values('weight',
                                                                    'bmi',
                                                                    'date').order_by('-date')
            strava_len = len(strava)
            body_len = len(body)

            if strava_len > 0 and body_len > 0:
                for i in range(strava_len):
                    strava_date = datetime.date(datetime.strptime(strava[i]['start_date'], "%Y-%m-%d %H:%M:%S+00:00"))
                    res[strava_date] = [strava[i]['average_speed'], str(round(strava[i]['distance']/1000, 2))+' km']
                i = 0
                for i in range(body_len):
                    body_date = datetime.date(body[i]['date'])
                    if body_date in res:
                        res[body_date] += [str(body[i]['weight']) + ' kg', 'bmi: ' + str(round(body[i]['bmi'], 2))]
                    else:
                        res[body_date] = [str(body[i]['weight']) + ' kg', 'bmi: ' + str(round(body[i]['bmi'], 2))]

                final_list = OrderedDict(reversed(sorted(res.items(), key=lambda x: x[0])))
            else:
                final_list = []

            data = {
                'list': final_list
            }
            return render(request, 'health/summary.html', {'data': data})
        else:
            return redirect('/')
    
    def post(self, request):
        pass


class ImportActivities(View):

    def get(self, request):
        if request.user.is_authenticated:
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
        else:
            return redirect('/')

    def post(self, request):
        pass


class Analytics(View):

    def get(self, request):
        if request.user.is_authenticated:
            from bokeh.layouts import layout
            from bokeh.embed import components
            from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter, RangeSlider, Span
            from bokeh.models.tools import HoverTool
            from bokeh.plotting import figure, output_file, show

            data = HealthData.objects.filter(user=request.user).values('weight', 'date')
            strava = ActivitiesStravaData.objects.filter(user=request.user).values('start_date', 'distance')[:40]

            if len(data) > 0:
                plot = figure(title="", x_axis_label="Date", x_axis_type='datetime', y_axis_label="Weight",
                            height=500,
                            sizing_mode="stretch_width",
                            toolbar_location="above",
                            tooltips="@y",
                            tools = "pan,wheel_zoom,box_zoom,reset,save")
                plot.toolbar.logo = None

                x = []
                y = []
                for i in range(len(data)):
                    x.append(data[i]['date'])
                    y.append(data[i]['weight'])

                # Research#########
                array = n.array(y)
                avg = n.average(array)
                max = n.max(array)
                amin = n.amin(array)
                ####################

                user_data = Profile.objects.filter(user=request.user).values('height', 'gender')[0]
                ideal = WeightCalculations.WeightIdeal(0, user_data['gender'], user_data['height'])

                avg_line = Span(location=avg,
                                line_width=3, line_color='red',
                                line_dash='dashed')

                ideal_line = Span(location=ideal[0],
                                line_width=3, line_color='green',
                                line_dash='dashed')

                plot.line(x, y, legend_label="Weight", line_width=2)
                plot.circle(x, y, size=10)
                plot.xaxis[0].formatter = DatetimeTickFormatter(months="%Y %m %d")
                plot.toolbar.active_scroll = "auto"
                plot.add_layout(avg_line)
                plot.add_layout(ideal_line)

                (div, script) = components(plot)

            else:
                div = 'Not enough data to calculate'
                script = ''

            if len(strava) > 0:
                dots = []
                distance = []
                for i in range(len(strava)):
                    dots.append(datetime.strptime(strava[i]['start_date'], "%Y-%m-%d %H:%M:%S+00:00"))
                    distance.append(strava[i]['distance'] / 1000)

                plot2 = figure(title="Activities", x_axis_type='datetime',
                            sizing_mode="stretch_width",
                            height=500,
                            tooltips='@y',
                            x_axis_label='Date',
                            y_axis_label='Distance',
                            toolbar_location="above",
                            tools="pan,wheel_zoom,box_zoom,reset,save")
                plot2.toolbar.logo = None

                plot2.circle(dots, distance, size=10)
                (div2, script2) = components(plot2)
            else:
                div2 = 'Add your activities from Strava'
                script2 = ''

            return render(request, 'health/analytics.html', {'div': div,
                                                            'div2': div2,
                                                            'script': script,
                                                            'script2': script2})
        else:
            return redirect('/')

    def post(self, request):
        pass
