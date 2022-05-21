from stravalib import Client
from django.conf import settings
from apps.health.models import ApiTokens

strava_data = settings.STRAVA_DATA


def CheckApiTokens(user):
    if ApiTokens.objects.filter(user=user).exist():
        pass


def StravaUrl(client_id=strava_data[0], redirect_url='https://mountaingrip.com/health/import'):
    client = Client()
    url = client.authorization_url(client_id=client_id, redirect_uri=redirect_url)

    return url


def StravaToken(client_id=strava_data[0], client_secret=strava_data[1], code=''):
    client = Client()
    access = client.exchange_code_for_token(client_id=client_id, client_secret=client_secret, code=code)
    client.access_token = access['access_token']
    client.refresh_token = access['refresh_token']
    expires_at = access['expires_at']

    return client

