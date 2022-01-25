from django.db import models
from django.contrib.auth.models import User


class Setting(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="settings", blank=False)
    # Profile and account settings
    show_trips_in_profile = models.BooleanField(default=True)
    # allow users to add post to profile    
    post_to_profile = models.BooleanField(default=True)
    # show age in profile
    age_in_profile = models.BooleanField(default=False)

