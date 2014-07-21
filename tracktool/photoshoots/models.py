import datetime

from django.conf import settings
from django.db import models

from contracts.models import Contract


ACCOUNT_CHOICES = (
    ('johanbeselaere@gmail.com', 'johanbeselaere@gmail.com'),
    ('bverhaegen@gmail.com', 'bverhaegen@gmail.com'),
    ('ahoravia@gmail.com', 'ahoravia@gmail.com'),
    ('byyoursite@gmail.com', 'byyoursite@gmail.com'),
    ('martinuskoolen@gmail.com', 'martinuskoolen@gmail.com'),
    ('combipano@gmail.com', 'combipano@gmail.com'),
    ('agoraviamx@gmail.com', 'agoraviamx@gmail.com'),
    ('aravianuvia@gmail.com', 'aravianuvia@gmail.com'),
    ('agoravianuvia@gmail.com', 'agoravianuvia@gmail.com'),
    ('agoraviabr@gmail.com', 'agoraviabr@gmail.com'),
)


class PhotoshootAppointment(models.Model):
    contract = models.ForeignKey(Contract, null=True)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    photographer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="photographer")
    account = models.EmailField(choices=ACCOUNT_CHOICES)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="creator", null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.contract.contract_number)

    def due_date_passed(self):
        if self.start_date_time.date() < datetime.date.today():
            return True
        return False