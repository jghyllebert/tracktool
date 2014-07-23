from apiclient.discovery import build
from django.conf import settings
from django.db import models
import httplib2
from timezone_field import TimeZoneField
from users.models import TrackUser


class WorldRegion(models.Model):
    name = models.CharField(max_length=5)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=20, blank=False)
    tva_percentage = models.IntegerField(blank=False)
    world_region = models.ForeignKey(WorldRegion)
    timezone = TimeZoneField()
    drive_folder_id = models.CharField(max_length=100,
                                       blank=True,
                                       help_text="A folder will be created when empty.")
    google_plus_document_id = models.URLField(blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.drive_folder_id:
            file_user = TrackUser.objects.get(pk=settings.USER_ID_GOOGLE_OAUTH)
            drive_service = build('drive', 'v2', http=file_user.credentials.authorize(httplib2.Http()))
            folder_body = {
                "title": self.name,
                "parents": [{"id": settings.DRIVE_PARENT_FOLDER_ID}],
                "mimeType": "application/vnd.google-apps.folder"
            }
            folder = drive_service.files().insert(body=folder_body).execute()

            #Save folder in Contract
            self.drive_folder_id = folder['id']
        super(Country, self).save()
