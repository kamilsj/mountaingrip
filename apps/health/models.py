from django.db import models
from django.contrib.auth.models import User


class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="health_data", blank=False)
    weight = models.FloatField(max_length=6)
    bmi = models.FloatField(blank=True)
    neck = models.FloatField(default=0, max_length=6)
    chest = models.FloatField(default=0, max_length=6)
    waist = models.FloatField(default=0, max_length=6)
    hip = models.FloatField(default=0, max_length=6)
    date = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.user


class ApiTokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_api_tokens", blank=False)
    access_token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)
    expire_at = models.DateTimeField()

    def __int__(self):
        return self.user


class ActivitiesStravaData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_strava_activities", blank=False)
    activity_id = models.BigIntegerField(null=True)
    name = models.CharField(max_length=1024)
    start_date = models.CharField(max_length=256, default='')
    distance = models.FloatField(null=True)
    moving_time = models.CharField(max_length=128)
    elapsed_time = models.CharField(max_length=128)
    total_elevation_gain = models.CharField(max_length=128, null=True)
    average_speed = models.FloatField(null=True)
    max_speed = models.FloatField(null=True)
    average_cadence = models.FloatField(null=True)
    average_watts = models.FloatField(null=True)
    elev_high = models.FloatField(null=True)
    elev_low = models.FloatField(null=True)
    average_temp = models.FloatField(null=True)
    calories = models.FloatField(null=True)

    def __str__(self):
        return self.name