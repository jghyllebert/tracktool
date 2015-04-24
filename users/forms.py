from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from users.models import TrackUser


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class UserForm(forms.ModelForm):

    class Meta:
        model = TrackUser
        fields = ('first_name', 'last_name', 'email')


class UserCreationForm(forms.ModelForm):
    """
    Form to create new users in the admin panel
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = TrackUser
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        #Check if passwords are equal
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Form to update users in adminpanel
    """
    password = ReadOnlyPasswordHashField(help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = TrackUser

    def clean_password(self):
        return self.initial["password"]


class ClientContactForm(forms.ModelForm):

    role = forms.CharField(max_length=75)
    notes = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = TrackUser
        fields = ('first_name', 'last_name', 'role', 'email', 'tel_number', 'address', 'notes')

    def __init__(self, *args, **kwargs):
        super(ClientContactForm, self).__init__(*args, **kwargs)
        self.fields['tel_number'].required = False

    def save(self, commit=True):
        model = super(ClientContactForm, self).save(commit)
        contact_group = Group.objects.get(name="customer_relations")
        contact_group.user_set.add(model)

        if commit:
            model.save()

        return model