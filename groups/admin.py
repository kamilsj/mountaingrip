from django.contrib import admin
from .models import Group, Thread, ThreadPost


@admin.register(Group)
class GroupsAdmin(admin.ModelAdmin):
    date_hierarchy = 'added_at'


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    date_hierarchy = 'added_at'


