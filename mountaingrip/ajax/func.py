from django.http import JsonResponse
from django.core import serializers
from start.models import TripJoined, Trip, Friend
from apps.groups.models import Thread
from apps.notifications.models import Notification
from func.notif import Notif
from django.contrib.auth.models import User
from django.db.models import Q



def AddFriend(request, id):
    user = request.user
    notif = Notif(2)
    if id > 0 and user.is_authenticated:
        who = User.objects.get(id=user.id)
        whom = User.objects.get(id=id)
        if not Friend.objects.filter((Q(who=who) & Q(whom=whom)) | (Q(who=whom) & Q(whom=who))).exists():
            if Friend.objects.create(who=who, whom=whom, accepted=0):
                notif.addNotif(who, whom, 0, '')
                data = {'OK': 1}
            else:
                data = {'OK': 0}
        else:
            data = {'OK': 0}
    else:
        data = {'OK': 0}

    return JsonResponse(data, safe=False)


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

    else:
        return False


def CheckNotifications(request):
    user = request.user
    data = {}
    count = Notification.objects.filter(Q(to=user) & Q(read=False)).count()
    if count > 0:
        data = {
            'count': count
        }
    return JsonResponse(data, safe=False)


