from django.contrib import admin
from .models import Group, GroupPic, GroupPost


@admin.register(Group)
class GroupsAdmin(admin.ModelAdmin):
    date_hierarchy = 'added_at'
