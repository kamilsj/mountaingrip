from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from health.models import HealthData
from start.models import Profile
from datetime import datetime

from func.AI.learn import WeightCalculations, CalcuclateChanges


class Suggestions(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
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


