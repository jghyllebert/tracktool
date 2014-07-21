from django.conf import settings
from django.db import models


class Notification(models.Model):
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


class Receivers(models.Model):
    notification = models.ForeignKey(Notification)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    has_read = models.BooleanField(default=False, blank=True)