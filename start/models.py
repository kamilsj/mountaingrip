from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Login(models.Model):
    userId = models.BigIntegerField()
    ipAddress = models.GenericIPAddressField()
    country = CountryField()
    date = models.DateTimeField()


class Tokens(models.Model):
    userId = models.BigIntegerField()
    token = models.CharField(max_length=255)
    activated = models.BooleanField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    userId = models.BigIntegerField()
    text = models.TextField(max_length=4096, blank=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):

    userId = models.BigIntegerField()
    postId = models.BigIntegerField(default=0)
    tripId = models.BigIntegerField(default=0)
    replyId = models.BigIntegerField()
    text = models.TextField(max_length=4096, blank=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Trip(models.Model):
    userId = models.BigIntegerField()
    title = models.CharField(max_length=256, blank=False)
    coverId = models.ImageField(upload_to='trip', blank=True)
    description = models.TextField(max_length=4096, blank=True)
    basePlace = models.CharField(max_length=256, blank=False)
    mountainName = models.CharField(max_length=256, blank=False)
    startDate = models.DateField(blank=False)
    endDate = models.DateField(blank=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.ManyToManyField(User)
    userId = models.BigIntegerField()
    picId = models.ImageField(upload_to='profile', blank=True)
    coverId = models.ImageField(upload_to='profile', blank=True)
    country = CountryField(blank=True)

    def __int__(self):
        return self.country

