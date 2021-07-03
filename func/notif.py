from apps.notifications.models import Notification
from django.contrib.auth.models import User


class Notif:

    '''
    1 - messages
    2 - friends
    3 - group post
    4 - profile post

    '''

    def __init__(self, cat):
        self.cat = cat

    def categories(self):
        if 0 < self.cat < 10:
            return self.cat
        else:
            return False

    def clean(self, id):
        pass

    def show_notif_short(self, user):
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



