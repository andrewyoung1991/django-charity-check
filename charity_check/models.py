from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError

from . import CHARITY_CHECK
from .util import verify_nonprofit, get_nonprofit_data


@python_2_unicode_compatible
class CharityCheck(models.Model):
    """ A class updated by a cronjob to validate charity data. It uses a dbm to search
    for an organizations EIN number and then validates the remaining data (name, city,
    state, country, deductability_code) with the values provided by the client.
    """
    ein = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=50)
    deductability_code = models.CharField(max_length=100)

    # if we are able to verify the data, we should sanitize it with the dbm values
    verified = models.BooleanField(default=False)
    sanitized = models.BooleanField(default=False)
    datetime_checked = models.DateTimeField(auto_now=True)
    charity = models.OneToOneField(CHARITY_CHECK["charity_model"])

    def __str__(self):
        return "<CharityCheck(ein={0})>".format(self.ein)
    __repr__ = __str__
    __unicode__ = __str__

    def sanitize_data(self):
        """ replace user provided data with dbm data
        """
        charity = get_nonprofit_data(self.ein)
        self.name = charity.name
        self.city = charity.city
        self.state = charity.state
        self.country = charity.country
        self.deductability_code = charity.dc

    def check_charity(self):
        """ check that a charity still has their non-profit status
        """
        verified = verify_nonprofit(
            ein=self.ein,
            name=self.name,
            city=self.city,
            state=self.state,
            dc=self.deductability_code)

        if verified and not self.sanitized:  # pragma: no branch
            self.sanitize_data()
            self.sanitized = True

        self.verified = verified


class CharityCheckException(models.Model):
    """ A utility class for capturing exceptions due to invalid user data
    """
    charity_check = models.ForeignKey("CharityCheck", related_name="exceptions")
    message = models.CharField(max_length=200)
    datetime_checked = models.DateTimeField(auto_now_add=True)
