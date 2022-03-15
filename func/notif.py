from apps.notifications.models import Notification
from django.contrib.auth.models import User


class Notif:

    '''
    1 - messages
    2 - friends
    3 - group post
    4 - profile post
    5 - trip joined
    6 - group followed
    7 - trip post
    8 - new desire the same as yours
    9 - 
    '''

    def __init__(self, cat):
        self.cat = cat

    def categories(self):
        if 0 < self.cat < 10:
            return self.cat
        else:
            return False

    def clear(self, id):
        pass

    def addNotif(self, user, to_whom, what, short):
        if 0 < self.cat < 9:
            trimmed = (short[:1020]+'...') if len(short) > 1020 else short
            cat = self.categories()
            Notification.objects.create(
                user=user,
                to=to_whom,
                what=what,
                short=trimmed,
                cat=cat
            )
        else:
            return 0



