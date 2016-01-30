import os
from datetime import timedelta

from django.conf import settings

basedir = os.path.abspath(os.path.dirname(__file__))

CHARITY_CHECK = getattr(settings, "CHARITY_CHECK", {})
# either a timedelta or a celery.CronTab
CHARITY_CHECK.setdefault("dbm_update_delta", timedelta(days=7))
CHARITY_CHECK.setdefault("charity_check_delta", timedelta(days=7))
CHARITY_CHECK.setdefault("dbm_location", os.path.join(basedir, "dbm"))
CHARITY_CHECK.setdefault("charity_model", settings.AUTH_USER_MODEL)


CHARTITY_CHECK_UPDATE_SCHEDULE = {
    "update_dbm": {
        "task": "dj_charity_check.tasks.get_dbm",
        "schedule": CHARITY_CHECK["dbm_update_delta"]
        }
    }
