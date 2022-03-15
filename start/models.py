from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone


class Login(models.Model):
    user = models.BigIntegerField(blank=False)
    ipAddress = models.GenericIPAddressField()
    country = CountryField()
    date = models.DateTimeField()


class Token(models.Model):
    user = models.BigIntegerField(blank=False)
    token = models.CharField(max_length=255)
    activated = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)


class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trip_author", blank=False)
    title = models.CharField(max_length=256, blank=False)
    cover = models.ImageField(upload_to='trip', blank=True, null=True)
    description = models.TextField(max_length=4096, blank=True, null=True)
    basePlace = models.CharField(max_length=256, blank=False)
    mountainName = models.CharField(max_length=256, blank=False)
    blat = models.FloatField(default=0)
    blng = models.FloatField(default=0)
    mlat = models.FloatField(default=0)
    mlng = models.FloatField(default=0)
    startDate = models.DateField(blank=False)
    endDate = models.DateField(blank=True, null=True)
    done = models.SmallIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TripJoined(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_joined_trip", blank=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_joined", default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.trip


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author", blank=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="posted_on_trip", blank=True, null=True)
    profile_id = models.PositiveBigIntegerField(default=0)
    text = models.TextField(max_length=4096, blank=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author", blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commented_post", default=0)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="commented_trip", default=0)
    reply_id = models.PositiveBigIntegerField(default=0)
    text = models.TextField(max_length=4096, blank=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Friend(models.Model):
    who = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="who_is_added", blank=False)
    whom = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="added_by_whom", blank=False)
    accepted = models.BooleanField(default=False)
    bla = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    pic = models.ImageField(upload_to='profile/pic/', default='', blank=True)
    cover = models.ImageField(upload_to='profile/cover/', default='', blank=True)
    gender = models.BooleanField(choices=((0, "Male"), (1, "Female")), default=0)
    birthday = models.DateField(blank=True, null=True)
    country = CountryField(blank=True)
    height = models.PositiveSmallIntegerField(blank=True, default=0)
    public_key = models.CharField(max_length=1024, blank=True, default='')
    private_key = models.CharField(max_length=1024, blank=True, default='')
    #SPECIAL TESTING FUNCTION CHANGED MANUALLY
    beta = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()+' ('+self.user.username+')'
        


