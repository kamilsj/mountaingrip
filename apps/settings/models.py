from django.db import models
from django.contrib.auth.models import User


class Settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="settings", blank=False)
    # Profile and account settings
    # allow users to add post to profile
    post_to_profile = models.BooleanField(default=True)
    # show age in profile
    age_in_profile = models.BooleanField(default=False)

