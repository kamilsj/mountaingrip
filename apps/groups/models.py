from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_author", blank=False)
    name = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=1024, blank=True, null=True)
    pic = models.ImageField(upload_to='group', null=True, blank=True)
    private = models.BooleanField(blank=False, default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name[:50]


class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="thread_author", blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="thread_in_group", blank=False)
    name = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=1024, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name[:50]


class ThreadPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_post_author", blank=False)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posted_in_thread", blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="thread_post_in_group", blank=False)
    text = models.TextField(max_length=4096, blank=False)
    attachments = models.BooleanField(default=False, blank=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class ThreadPic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_pic_author", blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="pic_in_group", blank=False)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="pic_in_thread", blank=False)
    post = models.ForeignKey(ThreadPost, on_delete=models.CASCADE, related_name="pic_in_post", blank=False)
    pic = models.ImageField(upload_to='group_post', null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)


class FollowedGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed_group", blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_followed", blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    
class FollowedThread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed_thread", blank=False)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="thread_followed", blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)


class PrivateGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="private_group_user", blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_private_users", blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
