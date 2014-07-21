from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from oauth2client.django_orm import CredentialsField


class UserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class TrackUser(AbstractBaseUser, PermissionsMixin):
    #User data
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    tel_number = models.BigIntegerField(blank=True, null=True,
                                        help_text="Only digits. First country code: eg. 32472444380")
    address = models.TextField(blank=True, null=True)

    #User options
    #True for first_name last_name
    #False for last_name first_name
    full_name_order = models.BooleanField(blank=True, default=True)
    email_notifications = models.BooleanField(blank=True, default=True)

    #Django necessities
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    #Google stuff
    credentials = CredentialsField()

    #Sales fields
    percentage_of_sales = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.pk])

    def get_full_name(self):
        if self.full_name_order:
            order = (self.first_name, self.last_name)
        else:
            order = (self.last_name, self.first_name)
        return "%s %s" % order

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return self.get_full_name()