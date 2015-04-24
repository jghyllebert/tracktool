from django import forms
from django.utils.safestring import mark_safe

from clients.models import Client


class ClientAddForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name', 'commercial_name', 'email', 'tva_number', 'billing_address', 'city', 'zip_code', 'country',
                  'website', 'google_plus_page', 'no_gplus_notes', 'additional_info')

    def __init__(self, *args, **kwargs):
        super(ClientAddForm, self).__init__(*args, **kwargs)
        self.fields['google_plus_page'].initial = "http://plus.google.com/"
        self.fields['no_gplus_notes'].help_text = mark_safe("If this client doesn't have a Google+ page, "
        "write down the reason. Steps to follow: "
        "<a target=\"_tab\" href=\"https://docs.google.com/a/nuntra.com/document/d/1K_S-c99kO2esYZ80hC-unV6jYYZzNDELVC6Wj3XInR4/edit\">Instructions</a>.")

    def clean_google_plus_page(self):
        gplus_url = self.cleaned_data.get('google_plus_page')
        gplus_notes = self.cleaned_data.get('no_gplus_notes')

        if not gplus_url or gplus_url == "http://plus.google.com/" and not gplus_notes:
            raise forms.ValidationError("Please fill in a reason.")
        return gplus_url