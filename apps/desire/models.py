from django.db import models
from django.contrib.auth.models import User


class Desire(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="desire_author", blank=False)
    desire = models.CharField(max_length=256, blank=False)
    how = models.IntegerField(default=0, blank=False)
    what = models.IntegerField(default=0, blank=False)
    lang = models.CharField(max_length=2, default="en", blank=False)
    added_at = models.DateTimeField(auto_now_add=True)


class DesireSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="desire_search", blank=False)
    desire = models.ForeignKey(Desire, on_delete=models.CASCADE, related_name="desire_id", blank=False)
    count = models.IntegerField(default=0, blank=False)
    added_at = models.DateTimeField(auto_now_add=True)