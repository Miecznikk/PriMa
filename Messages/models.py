from django.db import models
from django.contrib.auth.models import User


class MessageLinkAttachment(models.Model):
    link = models.CharField(max_length=255, null=False, blank=False)
    link_text = models.CharField(max_length=15, null=False, blank=False)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sender', null=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='receiver', null=True)

    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)

    created = models.DateTimeField(auto_now=True)

    attachment = models.ForeignKey(MessageLinkAttachment, on_delete=models.CASCADE, null=True, blank=True)
