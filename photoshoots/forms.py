from django import forms
from django.contrib.auth import get_user_model

from photoshoots.models import PhotoshootAppointment


User = get_user_model()


class CreateAppointment(forms.ModelForm):

    class Meta:
        model = PhotoshootAppointment
        fields = ('start_date_time', 'end_date_time', 'description', 'photographer', 'account',)

    def __init__(self, **kwargs):
        super(CreateAppointment, self).__init__(**kwargs)

        self.fields['photographer'].queryset = User.objects.filter(groups__name="photographer")


class PhotoShootComplete(forms.ModelForm):
    pois_uploaded = forms.BooleanField()
    panos_uploaded = forms.BooleanField()
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PhotoshootAppointment
        fields = ('id',)