from django.contrib import admin
from .models import Profile, Trip, Comment, Post


admin.site.site_header = 'Mountain Grip'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Trip)
class TripsAdmin(admin.ModelAdmin):
    date_hierarchy = 'added_at'


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    date_hierarchy = 'added_at'


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    date_hierarchy = "added_at"


