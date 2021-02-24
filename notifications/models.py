from django.db import models
from django.contrib.auth.models import User


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notif_user', blank=False)

    
    