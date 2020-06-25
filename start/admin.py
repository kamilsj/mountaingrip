from django.contrib import admin
from .models import Profile, Trip, Comment


admin.site.site_header = 'Mountain Grip'

@admin.register(Profile)
class ActivitiesAdmin(admin.ModelAdmin):
    pass

@admin.register(Trip)
class TripsAdmin(admin.ModelAdmin):
    date_hierarchy = 'added_at'

@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    date_hierarchy = 'added_at'