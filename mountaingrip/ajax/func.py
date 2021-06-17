from django.http import JsonResponse
from django.core import serializers
from start.models import TripJoined, Trip, Friend
from apps.groups.models import Thread
from django.contrib.auth.models import User
from django.db.models import Q


def AddFriend(request, id):
    user = request.user
    if id > 0 and user.is_authenticated:
        who = User.objects.get(id=user.id)
        whom = User.objects.get(id=id)
        if not Friend.objects.filter((Q(who=who) & Q(whom=whom)) | (Q(who=whom) & Q(whom=who))).exists():
            if Friend.objects.create(who=who, whom=whom, accepted=0):
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