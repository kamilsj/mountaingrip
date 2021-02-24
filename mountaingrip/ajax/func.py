from django.http import JsonResponse
from django.core import serializers
from start.models import TripJoined, Trip
from groups.models import Thread
from django.contrib.auth.decorators import login_required



def AddFriend(request, id):
    pass



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