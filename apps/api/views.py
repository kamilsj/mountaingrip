from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from apps.health.models import HealthData
from start.models import Profile
from apps.notifications.models import Notification
from datetime import datetime

from .serializers import UserSerializer
from func.AI.learn import WeightCalculations, CalcuclateChanges


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

    def get(self, request, query):
        pass


class Suggestions(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ''' showing users nice suggestions of what to do, to read, to ask in the website '''
        data = {
            'groups': [
                {'id': 'Welcome!'},
                {'id': 'It\'s work in progress. Many things still do not work. '}
            ]
        }


        return Response(data)



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
    permission_classes = [IsAuthenticated]