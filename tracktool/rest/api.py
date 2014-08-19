from tastypie.resources import ModelResource
from clients.models import Client, ContactPerson


class ClientResource(ModelResource):

    class Meta:
        queryset = Client.objects.all()
        resource_name = 'client'