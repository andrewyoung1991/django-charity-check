import os
from unittest import mock

import pytest

from charity_check import CHARITY_CHECK, util


@mock.patch("charity_check.util.urlopen")
@mock.patch("charity_check.util.zipfile.ZipFile")
def test_downloading_irs_nonprofit_data(mock_zipfile, mock_urlopen):
    mock_ctx_manager = mock.Mock()
    mock_ctx_manager.__enter__ =  mock.Mock(read=mock.Mock(return_value=""))
    mock_ctx_manager.__exit__ =  mock.Mock()

    mock_urlopen.return_value = mock_ctx_manager

    util.make_dbm()
    mock_urlopen.assert_called_with(util.IRS_NONPROFIT_DATA_URL)
    mock_extract = mock_zipfile.return_value.__enter__().extract
    mock_extract.assert_called_with(member=util.TXT_FILE_NAME,
                                            path=CHARITY_CHECK["dbm_location"])

    ein = "000003154"
    charity = util.get_nonprofit_data(ein)
    assert charity.name == "Oakleaf Forest Tenant Management"
    assert charity.city == "Norfolk"
    assert charity.state == "VA"
    assert charity.country == "United States"
    assert charity.dc == "PC"
    assert os.path.exists(util._publication78_dbm)
