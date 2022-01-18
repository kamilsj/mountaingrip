from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.db.models import Q
from apps.health.models import HealthData
from start.models import Profile, Trip
from apps.notifications.models import Notification

from .serializers import UserSerializer
from func.AI.learn import WeightCalculations, CalcuclateChanges
from func.notif import Notif


class Notifications(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        pass

    def post(self, request, id):
        pass


class Autocomplete(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, what=''):
        data = {}
        suggestions = []
        excluded = []
        if request.method == 'GET':
            q = request.GET['query']
            if what == 'bp':
                pass
            elif what == 'mn':
                pass
            else:
                ''' write an intelligent query to predict the most common questions '''
                places = Trip.objects.filter(Q(basePlace__startswith=q) | Q(mountainName__startswith=q)).all()
                for place in places:
                    if not place.basePlace in excluded:
                        suggestions.append({'value': place.basePlace, 'data': place.id})
                        excluded.append(place.basePlace)
                    if not place.mountainName in excluded:
                        suggestions.append({'value': place.mountainName, 'data': place.id})
                        excluded.append(place.mountainName)
                data = {
                'query': q,
                'suggestions': suggestions
            }
        return Response(data)



class AutocompleteInbox(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {}
        suggestions = []
        if request.method == 'GET':
            q = request.GET['query']
            '''suggestions users in new message user box'''
            users = User.objects.filter(Q(first_name__startswith=q) | Q(last_name__startswith=q)).all()
            for user in users:
                suggestions.append(
                    {'value': user.first_name + ' ' + user.last_name + ' (' + user.username + ')', 'data': user.id})

            data = {
                'query': q,
                'suggestions': suggestions
            }

        return Response(data)


class Suggestions(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ''' showing users nice suggestions of what to do, to read, to ask in the website '''
        ''' trips, users and some nice groups ... '''
        data = {
            'groups': [
                {'id': 'Welcome!'},
                {'id': 'It\'s work in progress. Many things still do not work. '}
            ]
        }

        return Response(data)

    def post(self, request):
        pass


class ActivitieData(APIView):
    pass


class ChartData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    calculations = WeightCalculations()

    def get(self, request):
        user = request.user
        health = HealthData.objects.filter(user=user).all().order_by('-id')[:10].values()
        label = []
        chartData = []
        weight = []

        profile = Profile.objects.get(user=user)

        if health.count() > 1:
            for healthData in health:
                label.append(healthData['date'].strftime("%d %b %y"))
                if healthData['bmi'] == 0:
                    if profile.height > 0 and profile.height < 250:
                        bmi = healthData['weight'] / (profile.height / 100) ** 2
                        HealthData.objects.filter(id=healthData['id']).update(bmi=bmi)
                        chartData.append(round(bmi, 2))
                else:
                    chartData.append(round(healthData['bmi'], 2))

                weight.append(healthData['weight'])
        else:
            label = health[0]['date'].strftime("%d %b %y")
            if health[0]['bmi'] > 0:
                chartData = round(health[0]['bmi'], 2)
            weight = health[0]['weight']

        [IdealWeight, bmi] = self.calculations.WeightIdeal(profile.gender, profile.height)

        data = {
            'label': label,
            'chartData': chartData,
            'bmi': round(bmi, 2),
            'weight': weight,
            'idealweight': round(IdealWeight, 2)
        }

        return Response(data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
