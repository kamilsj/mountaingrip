from django.http import JsonResponse
from django.core import serializers
from start.models import TripJoined, Trip


def AddFriend(request, id):
    pass


def JoinTrip(request, id):
    user = request.user
    if id > 0:
        if Trip.objects.filter(id=id).exists():
            trip = Trip.objects.get(id=id)
            if not TripJoined.objects.filter(user=user, trip=trip).exists():
                if TripJoined.objects.create(user=user, trip=trip):
                    return True
                else:
                    return False

    else:
        return False


def AddPost(request):
    pass


def CheckMessages(request):
    pass