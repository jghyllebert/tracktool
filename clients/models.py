from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from project_settings.models import Country


class Client(models.Model):
    # General data
    name = models.CharField(max_length=100)
    commercial_name = models.CharField(max_length=100)
    email = models.EmailField(blank=False)
    account_manager = models.ForeignKey(settings.AUTH_USER_MODEL)
    google_plus_page = models.URLField(blank=True, null=True)
    no_gplus_notes = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)
    additional_info = models.TextField(blank=True)

    #Invoice data
    tva_number = models.CharField(max_length=25, blank=False, null=False)
    billing_address = models.TextField(blank=False)
    city = models.CharField(max_length=25, blank=False)
    zip_code = models.CharField(max_length=10, blank=False)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('client_detail', args=[str(self.id)])


class ContactPerson(models.Model):
    client = models.ForeignKey(Client, related_name="contacts")
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    role = models.CharField(max_length=75, blank=False)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.user.get_full_name()