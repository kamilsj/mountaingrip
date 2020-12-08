from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_author", blank=False)
    name = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=1024, blank=True, null=True)
    pic = models.ImageField(upload_to='group', null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)


class GroupPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_post_author", blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="posted_in_group", blank=False)
    text = models.TextField(max_length=4096, blank=False)
    added_at = models.DateTimeField(auto_now_add=True)


class GroupPic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_pic_author", blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="pic_in_group", blank=False)
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name="pic_in_post", blank=False)
    pic = models.ImageField(upload_to='group_post', null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
