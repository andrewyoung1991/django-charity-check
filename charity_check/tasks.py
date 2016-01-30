import celery

from django.utils import timezone
from django.core.exceptions import ValidationError

from . import CHARITY_CHECK
from .models import CharityCheck, CharityCheckException
from .util import make_dbm


@celery.shared_task
def get_dbm():  # pragma: no cover
    make_dbm()


@celery.shared_task
def check_charities():
    delta = timezone.now() - CHARITY_CHECK["charity_check_delta"]
    errored_checks = set()

    qs = CharityCheck.objects.filter(datetime_checked__gte=delta)
    for charity_check in qs.iterator():
        try:
            charity_check.check_charity()
            charity_check.save()
            charity_check.exceptions.all().delete()
        except ValidationError as err:
            errored_checks.add(charity_check.id)
            CharityCheckException.objects.create(
                charity_check=charity_check,
                message=str(err)
                )

    errored_checks = CharityCheck.objects.filter(id__in=errored_checks)
    errored_checks.update(verified=False, sanitized=False)
