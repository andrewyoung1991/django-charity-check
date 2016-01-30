import os

DEBUG = True

SECRET_KEY = "unguessable"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "charity_check",
    ]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "dj_charity_check",
        "USER": "postgres"
        }
    }

ROOT_URLCONF = "tests.urls"
SITE_ID = 1

CHARITY_CHECK = {
    "dbm_location": os.path.dirname(__file__)
    }

CELERY_ALWAYS_EAGER = True
