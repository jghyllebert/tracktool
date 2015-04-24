from django.db import models
from django.utils.text import slugify
from django.conf import settings

from project_settings.models import Country


class Product(models.Model):
    name = models.CharField(max_length=75)
    slug = models.SlugField(blank=True)
    flow = models.TextField(
        help_text="To insert the options in the flow, add the placeholder: <b>%s</b>" % settings.FLOW_OPTIONS_PLACEHOLDER
    )
    options = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Product, self).save()


class BasePricePerCountry(models.Model):
    product = models.ForeignKey(Product)
    country = models.ForeignKey(Country)
    base_price = models.PositiveIntegerField()