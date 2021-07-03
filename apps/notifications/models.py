from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_notifies', blank=False)
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_is_notified', blank=False)
    what = models.PositiveBigIntegerField(default=0, blank=False)
    cat = models.PositiveSmallIntegerField(default=0, blank=False)
    short = models.CharField(max_length=1024, default='', blank=True)
    read = models.BooleanField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
