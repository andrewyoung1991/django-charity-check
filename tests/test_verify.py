from unittest import mock
from django.core.exceptions import ValidationError

import pytest

from charity_check.util import verify_nonprofit


@mock.patch("charity_check.util.dbm")
def test_validating_user_data(mock_dbm):
    fake_response = {
        "000003154":
        b"Oakleaf Forest Tenant Management|Norfolk|VA|United States|PC"
        }
    mock_dbm.open.return_value.__enter__.return_value = fake_response

    ein = "000003154"
    verified = verify_nonprofit(ein)
    assert verified


@mock.patch("charity_check.util.dbm")
def test_validating_user_data_kwargs(mock_dbm):
    fake_response = {
        "000003154":
        b"Oakleaf Forest Tenant Management|Norfolk|VA|United States|PC"
        }
    mock_dbm.open.return_value.__enter__.return_value = fake_response

    ein = "000003154"
    verified = verify_nonprofit(ein, name="Oakleaf Forest Tenant Management")
    assert verified


@mock.patch("charity_check.util.dbm")
def test_validating_user_data_kwargs_error(mock_dbm):
    fake_response = {
        "000003154":
        b"Oakleaf Forest Tenant Management|Norfolk|VA|United States|PC"
        }
    mock_dbm.open.return_value.__enter__.return_value = fake_response

    ein = "000003154"
    with pytest.raises(ValidationError) as err:
        verify_nonprofit(ein, name="Oakleaf Forest Tenant")
    assert err.value.message_dict == {"name": ["did not match IRS records"]}


@mock.patch("charity_check.util.dbm")
def test_validating_user_data_key_error(mock_dbm):
    fake_response = {
        "000003154":
        b"Oakleaf Forest Tenant Management|Norfolk|VA|United States|PC"
        }
    mock_dbm.open.return_value.__enter__.return_value = fake_response

    ein = "00003154"
    verified = verify_nonprofit(ein, name="Oakleaf Forest Tenant")
    assert verified is False


@mock.patch("charity_check.util.dbm")
def test_validating_user_data_dc_error(mock_dbm):
    fake_response = {
        "000003154":
        b"Oakleaf Forest Tenant Management|Norfolk|VA|United States|PC"
        }
    mock_dbm.open.return_value.__enter__.return_value = fake_response

    ein = "000003154"
    with pytest.raises(ValidationError) as err:
        verify_nonprofit(ein, dc="pp")
    assert err.value.message_dict == {"deductability_code": ["did not match IRS records"]}
