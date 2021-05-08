from django.http import JsonResponse
from django.core import serializers
from start.models import TripJoined, Trip, Friends
from apps.groups.models import Thread

from django.db.models import Q



def AddFriend(request, id):
    user = request.user
    if id > 0 and user.is_authenticated:
        if not Friends.objects.filter((Q(who=user.id) & Q(whom=id)) | (Q(who=id) & Q(whom=user.id))).exists():
            if Friends.objects.create(who=user.id, whom=id, accepted=0):
                return True
            else:
                return False
        else:
            return False
    else:
        return False



def JoinTrip(request, id):
    user = request.user
    if id > 0 and user.is_authenticated:
        if Trip.objects.filter(id=id).exists():
            trip = Trip.objects.get(id=id)
            if not TripJoined.objects.filter(user=user, trip=trip).exists():
                if TripJoined.objects.create(user=user, trip=trip):
                    return True
                else:
                    return False

    else:
        return False


def AddPost(request, id):
    pass



def CheckMessages(request, id):
    user = request.user
    data = []
    if id > 0:
       return JsonResponse(data, safe=False)