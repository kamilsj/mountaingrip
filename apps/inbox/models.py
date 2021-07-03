from django.db import models
from django.contrib.auth.models import User


class InboxConf(models.Model):
    pass


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="from_message", blank=False)
    to = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="to_message", blank=False)
    text = models.TextField(max_length=4096, blank=False)
    title = models.TextField(max_length=512, blank=True, null=True)
    conversation = models.CharField(max_length=64, null=False)
    read = models.BooleanField(default=False)
    attachments = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)


class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.DO_NOTHING, related_name='message_files')