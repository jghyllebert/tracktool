from django.contrib import admin

from .models import Client, ContactPerson


# Register your models here.
admin.site.register(Client)
admin.site.register(ContactPerson)