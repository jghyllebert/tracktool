from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as GenericUserAdmin

from users.models import TrackUser as User
from users.forms import UserChangeForm, UserCreationForm


class UserAdmin(GenericUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('groups', 'is_admin', 'is_superuser', 'is_staff', 'email_notifications')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
