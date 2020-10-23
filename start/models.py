from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from birthday import fields


class Login(models.Model):
    user = models.BigIntegerField(blank=False)
    ipAddress = models.GenericIPAddressField()
    country = CountryField()
    date = models.DateTimeField()


class Token(models.Model):
    user = models.BigIntegerField(blank=False)
    token = models.CharField(max_length=255)
    activated = models.BooleanField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)


class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trip_author", blank=False)
    title = models.CharField(max_length=256, blank=False)
    cover = models.ImageField(upload_to='trip', blank=True)
    description = models.TextField(max_length=4096, blank=True)
    basePlace = models.CharField(max_length=256, blank=False)
    mountainName = models.CharField(max_length=256, blank=False)
    blat = models.FloatField(default=0)
    blng = models.FloatField(default=0)
    mlat = models.FloatField(default=0)
    mlng = models.FloatField(default=0)
    startDate = models.DateField(blank=False)
    endDate = models.DateField(blank=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author", blank=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="posted_on_trip", default=0)
    profile_id = models.BigIntegerField(default=0)
    text = models.TextField(max_length=4096, blank=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author", blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commented_post", default=0)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="commented_trip", default=0)
    reply_id = models.BigIntegerField(default=0)
    text = models.TextField(max_length=4096, blank=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    pic = models.ImageField(upload_to='profile', blank=True)
    cover = models.ImageField(upload_to='profile', blank=True)
    birthday = fields.BirthdayField()
    country = CountryField(blank=True)
    

    def __str__(self):
        return self.user.get_full_name()+' ('+self.user.username+')'
        


