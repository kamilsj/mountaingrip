from apps.notifications.models import Notification
from django.contrib.auth.models import User


class Notif:

    def __init__(self, cat):
        self.cat = cat

    def categories(self):
        if 0 < self.cat < 10:
            return self.cat
        else:
            return False

    def addNotif(self, who, where, what):
        if User.objects.filter(user = who).exists():
            if 0 < self.cat < 9:
                trimed = (what[:1020]+'...') if len(what) > 1020 else where
                cat = self.categories()
                Notification.objects.create(
                    user=who,
                    where=where,
                    what=trimed,
                    cat=cat
                )
            else:
                return 0



