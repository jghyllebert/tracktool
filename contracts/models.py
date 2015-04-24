import hashlib
import time

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from clients.models import Client


def _createHash():
    """This function generate 10 character long hash"""
    hash = hashlib.sha1()
    hash.update(str(time.time()))
    return hash.hexdigest()[:-10]


class Contract(models.Model):
    client = models.ForeignKey(Client, null=True)
    slug = models.SlugField(default=_createHash)
    contract_number = models.IntegerField()
    contract_date = models.DateField(help_text="Format YYYY-MM-DD")
    shoot_address = models.TextField()
    shoot_city = models.CharField(max_length=25, blank=False)
    shoot_zip_code = models.CharField(max_length=10, blank=False)

    #checks
    is_sent = models.BooleanField(blank=True, default=False)
    is_paid = models.BooleanField(blank=True, default=False)
    contract_started = models.DateTimeField(auto_now_add=True)
    invoice_sent = models.DateTimeField(blank=True, null=True)
    date_is_paid = models.DateTimeField(blank=True, null=True)

    #payment stuff
    amount_paid = models.DecimalField(default=0.00, decimal_places=2, max_digits=8)  # imprest, partial payments
    total_cost = models.DecimalField(
        help_text="AMEA: price exclusive VAT. AMER: inclusive VTA",
        decimal_places=2,
        max_digits=8
    )
    payment_options = models.TextField(blank=True)

    #Google stuff
    drive_folder_id = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if self.amount_paid >= self.total_cost:
            import datetime
            self.is_paid = True
            self.date_is_paid = datetime.datetime.now()
        super(Contract, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('contract_detail', args=[str(self.pk)])

    def get_active_photoshoot(self):
        return self.photoshootappointment_set.get(active=True)


class Payment(models.Model):
    contract = models.ForeignKey(Contract)
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    reference = models.TextField(blank=True)
    inputter = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_on = models.DateTimeField(auto_now_add=True)