from tracktool.tracktool.settings import *


SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': ''
    }
}

STATIC_ROOT = ''
STATIC_URL = ''


REDIRECT_URL = ""