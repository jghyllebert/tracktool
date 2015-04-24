from django.contrib import admin

from project_settings.models import Country, WorldRegion


admin.site.register(Country)
admin.site.register(WorldRegion)