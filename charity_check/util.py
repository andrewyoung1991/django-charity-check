try:
    import anydbm as dbm
except ImportError:
    import dbm

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from io import BytesIO

import csv
import zipfile
import os
import collections

from django.core.exceptions import ValidationError

from . import CHARITY_CHECK


# Keep these variables up-to-date

# the url of the IRS publication 78, assumed to
# be a zip folder containing a text file of
# publication 78, in the format:
#    EIN|name|city|state abbreviation|country|deductability code
IRS_NONPROFIT_DATA_URL = "http://apps.irs.gov/pub/epostcard/data-download-pub78.zip"

# the name that the irs gives to the text file
# version of publication 78 contained in their
# zip file download
TXT_FILE_NAME = "data-download-pub78.txt"

# dynamically generated path to the irs publication
# 78 file, do not edit/change this variable.
_irs_data_path = os.path.join(CHARITY_CHECK["dbm_location"], TXT_FILE_NAME)

# name of the database/dbm to generate from
# publication 78
PUBLICATION78_DBM_NAME = "IRSPublication78.dbm"

# dynamically generate path to dbm file
_publication78_dbm = os.path.join(CHARITY_CHECK["dbm_location"], PUBLICATION78_DBM_NAME)


class IRSNonprofitData:
    def __init__(self):
        self.pub78 = None

    def _download_irs_nonprofit_data(self):
        with urlopen(IRS_NONPROFIT_DATA_URL) as irs_url_data:
            data = BytesIO(irs_url_data.read())
            with zipfile.ZipFile(data) as zipped:
                zipped.extract(member=TXT_FILE_NAME, path=CHARITY_CHECK["dbm_location"])

    def __enter__(self):
        self._download_irs_nonprofit_data()
        self.pub78 = open(_irs_data_path, "r")
        reader = csv.reader(self.pub78, delimiter="|")
        return reader

    def __exit__(self, exc_type, exc_value, traceback):
        self.pub78.close()

_irs_non_profit_data = IRSNonprofitData()


def make_dbm():
    """ Reads a new irs non profit data file into a local dbm
    """
    with _irs_non_profit_data as irs_data:
        with dbm.open(_publication78_dbm, "n") as db:
            for row in irs_data:
                if not len(row):  # pragma: no cover
                    continue
                ein, data = row[0], row[1:]
                data = "|".join(data)
                db[ein] = data


Charity = collections.namedtuple("Charity", ["name", "city", "state", "country", "dc"])


def get_nonprofit_data(ein):
    """
    """
    with dbm.open(_publication78_dbm, "r") as db:
        output = map(lambda x: x.decode(), db[ein].split(b"|"))
    return Charity(*output)


def verify_nonprofit(ein, **kwargs):
    """
    """
    try:
        # create a list of the nonprofit"s info
        data = get_nonprofit_data(ein)
    except KeyError:
        return False

    dc = kwargs.pop("dc", None)
    for key, value in kwargs.items():
        match = getattr(data, key, None)
        if not value.lower() == match.lower():
            raise ValidationError({key: "did not match IRS records"})
    if dc is not None:
        dcs = dc.lower().split(",")
        local_dcs = data.dc.lower().split(",")
        for code in dcs:
            if not code in local_dcs:
                raise ValidationError({"deductability_code": "did not match IRS records"})

    return True
