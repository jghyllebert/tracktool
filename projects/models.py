from django.conf import settings
from django.db import models

from contracts.models import Contract
from products.models import Product


PROJECT_STATES = (
    ('sales', 'Sales'),
    ('photographer', 'Photographer'),
    ('production', 'Production'),
    ('invoicing', 'Invoicing'),
    ('finished', 'Finished'),
)


class Project(models.Model):
    contract = models.ForeignKey(Contract)
    product = models.ForeignKey(Product)
    notes = models.TextField(blank=True)
    flow = models.TextField(blank=True)
    current_state = models.CharField(
        max_length=30,
        choices=PROJECT_STATES,
        default='sales'
    )

    # track fields
    start_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    is_ended = models.BooleanField(blank=True, default=False)
    end_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        if self.is_ended:
            from datetime import datetime
            self.end_date = datetime.now()

    def __unicode__(self):
        return str(self.contract.contract_number)


class ProjectState(models.Model):
    project = models.ForeignKey(Project, related_name='states')
    datestamp = models.DateTimeField(auto_now_add=True)
    state = models.CharField(
        max_length=30,
        choices=PROJECT_STATES,
        default='sales'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.get_state_display()