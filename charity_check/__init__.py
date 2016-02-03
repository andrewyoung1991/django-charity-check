from datetime import timedelta
import os

from django.conf import settings


basedir = os.path.abspath(os.path.dirname(__file__))

CHARITY_CHECK = getattr(settings, "CHARITY_CHECK", {})
CHARITY_CHECK.setdefault("dbm_location", basedir)
CHARITY_CHECK.setdefault("charity_model", settings.AUTH_USER_MODEL)
CHARITY_CHECK.setdefault("charity_check_delta", timedelta(days=7))
CHARITY_CHECK.setdefault("user_charity_relation", "id")
