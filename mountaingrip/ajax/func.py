from django.http import JsonResponse, HttpResponse
from django.core import serializers
from start.models import TripJoined, Trip, Friend
from apps.groups.models import Thread
from apps.notifications.models import Notification
from func.notif import Notif
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import gettext as _

from start.templatetags.add_func import show_avatar_small


def ShowSuggestions(request):
    pass


def ShowTrips(request):
    pass


def ShowNotifications(request):
    user = request.user
    div = '<div class="list-group list-group-flush w-100">'
    middle = ''
    end_div = '</div>'
    end = ''
    if user.is_authenticated:
        notif = Notification.objects.filter(to=user, read=False).order_by('-id').all()[:20]
        if notif.count() == 0:
            notif = Notification.objects.filter(to=user).order_by('-id').all()[:5]
        # update read
        Notification.objects.filter(to=user, read=False).update(read=True)
        for n in notif:
            # somebody sent you a message
            whom = show_avatar_small(n.user.id)

            if not n.read:
                add = ' list-group-item-primary '
            else:
                add = ' list-group-item-light '

            middle += '<div class="list-group-item '+add+' d-flex align-items-center"> \n'

            if n.cat == 1:
                middle += '<a href="/start/profile/'+str(n.user.id)+'/"><img title="'+whom['name']+'" src="'+whom['pic']+'" class="img-rounded rounded-circle tp m-2" style="width:40px; height: 40px; object-fit: cover;"></a>\n' \
                          '<a href="/inbox/message/'+str(n.what)+'" class="ml-2">\n' \
                          '<small class="text_muted">'+_(' sent you a message: ')+'<br><b>'+str(n.short)+'</b></small></a>\n'
            # somebody added you as a friend
            elif n.cat == 2:
                middle += '<a href="/start/profile/'+str(n.user.id)+'/"><img title="' + whom['name'] + '" src="' + whom['pic'] + '" class="img-rounded rounded-circle tp" style="width:40px; height: 40px; object-fit: cover;"></a>\n'
                middle += '<span class="ml-2">'+_(' added you as a friend.')+'</span>\n'
            # somebody added a post to your group
            elif n.cat == 3:
                middle += '<a href="/start/profile/'+str(n.user.id)+'/"><img title="'+whom['name']+'" src="'+whom['pic']+'" class="img-rounded rounded-circle tp" style="width:40px; height: 40px; object-fit: cover;"></a>\n'
            # somebody added a post to your profile
            elif n.cat == 4:
                middle += '<a href="/start/profile/'+str(n.user.id)+'/"><img title="'+whom['name']+'" src="'+whom['pic']+'" class="img-rounded rounded-circle tp" style="width:40px; height: 40px; object-fit: cover;"></a>\n'
            # somebody followed your group
            elif n.cat == 5:
                middle += '<a href="/start/profile/'+str(n.user.id)+'/"><img title="'+whom['name']+'" src="'+whom['pic']+'" class="img-rounded rounded-circle tp" style="width:40px; height: 40px; object-fit: cover;"></a>\n'
            # somebody added a post to your trip
            elif n.cat == 6:
                middle += '<a href="/start/profile/'+str(n.user.id)+'/"><img title="'+whom['name']+'" src="'+whom['pic']+'" class="img-rounded rounded-circle tp" style="width:40px; height: 40px; object-fit: cover;"></a>\n'
            elif n.cat == 7:
                middle += '<a href="/start/profile/'+str(n.user.id)+'/"><img title="'+whom['name']+'" src="'+whom['pic']+'" class="img-rounded rounded-circle tp" style="width:40px; height: 40px; object-fit: cover;"></a>\n'
            elif n.cat == 8:
                middle += '<a href="/start/profile/'+str(n.user.id)+'/"><img title="'+whom['name']+'" src="'+whom['pic']+'" class="img-rounded rounded-circle tp" style="width:40px; height: 40px; object-fit: cover;"></a>\n'
            elif n.cat == 9:
                middle += '<a href="/start/profile/'+str(n.user.id)+'/"><img title="'+whom['name']+'" src="'+whom['pic']+'" class="img-rounded rounded-circle tp" style="width:40px; height: 40px; object-fit: cover;"></a>\n'
            else:
                pass

            middle += '</div>'

        end = div+middle+end_div
    else:
        end = '<p><b>Something went wrong!</b></p>'
        
    return HttpResponse(end)


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
    notif = Notif(5)
    if id > 0 and user.is_authenticated:
        if Trip.objects.filter(id=id).exists():
            trip = Trip.objects.get(id=id)
            if not TripJoined.objects.filter(user=user, trip=trip).exists():
                try:
                    obj = TripJoined.objects.create(user=user, trip=trip)
                    notif.addNotif(user, trip.user, obj.id, '')
                    return True
                except:
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


