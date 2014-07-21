from django.contrib import admin

from .models import Country, WorldRegion


admin.site.register(Country)
admin.site.register(WorldRegion)