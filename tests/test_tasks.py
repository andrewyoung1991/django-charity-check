from datetime import timedelta
from django.utils import timezone

from unittest import mock

import pytest

from charity_check import tasks, models


@mock.patch("charity_check.util.dbm")
@pytest.mark.django_db
def test_check_charities(mock_dbm, charity):
    fake_response = {
        "000003154":
        b"Oakleaf Forest Tenant Management|Norfolk|VA|United States|PC"
        }
    mock_dbm.open.return_value.__enter__.return_value = fake_response
    checker = models.CharityCheck.objects.create(
        ein="000003154",
        name="Oakleaf Forest Tenant Management",
        city="Norfolk",
        state="VA",
        country="United States",
        deductability_code="PC",
        charity=charity,
        datetime_checked=timezone.now() - timedelta(days=30)
        )
    tasks.check_charities()

    checker.refresh_from_db()
    assert checker.verified
    assert checker.sanitized


@mock.patch("charity_check.util.dbm")
@pytest.mark.django_db
def test_check_charities_error(mock_dbm, charity):
    fake_response = {
        "000003154":
        b"Oakleaf Forest Tenant Management|Norfolk|VA|United States|PC"
        }
    mock_dbm.open.return_value.__enter__.return_value = fake_response
    checker = models.CharityCheck.objects.create(
        ein="000003154",
        name="Forest Tenant Management",
        city="Norfolk",
        state="VA",
        country="United States",
        deductability_code="PC",
        charity=charity,
        datetime_checked=timezone.now() - timedelta(days=30)
        )
    tasks.check_charities()

    checker.refresh_from_db()
    assert not checker.verified
    assert not checker.sanitized
    assert checker.exceptions.first().message == "{'name': ['did not match IRS records']}"
