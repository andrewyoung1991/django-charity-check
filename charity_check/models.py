import hashlib
import os

from django.db import models
from django.conf import settings
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError

from . import CHARITY_CHECK
from .util import verify_nonprofit, get_nonprofit_data


def verification_document_handler(instance, filename):
    md5 = hashlib.md5()
    filename, ext = os.path.splitext(filename)
    md5.update(filename.encode() + settings.SECRET_KEY.encode())
    filename = str(md5.hexdigest())
    path = "{0}/{1}{2}".format(instance.charity.id, filename, ext)
    return os.path.join("charity-check-documents", path)


@python_2_unicode_compatible
class CharityCheck(models.Model):
    """ A class updated by a cronjob to validate charity data. It uses a dbm to search
    for an organizations EIN number and then validates the remaining data (name, city,
    state, country, deductability_code) with the values provided by the client.
    """
    PENDING = 0
    FAILED = 1
    VERIFIED = 2
    VERIFICATION_STATUSES = (
        (PENDING, "pending"),
        (FAILED, "failed"),
        (VERIFIED, "verified")
        )

    ein = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=50)
    deductability_code = models.CharField(max_length=100)

    # if we are able to verify the data, we should sanitize it with the dbm values
    verification_status = models.PositiveSmallIntegerField(choices=VERIFICATION_STATUSES,
                                                            default=PENDING)
    verified = models.BooleanField(default=False)
    sanitized = models.BooleanField(default=False)
    datetime_checked = models.DateTimeField(auto_now=True)
    charity = models.OneToOneField(CHARITY_CHECK["charity_model"])
    verification_document = models.FileField(upload_to=verification_document_handler,
                                                null=True, blank=True)
    verification_document_verified = models.BooleanField(default=False)

    def __str__(self):
        args = (self.ein, self.name, self.verified)
        return "<CharityCheck(ein={0}, name={1}, verified={2})>".format(*args)
    __repr__ = __str__
    __unicode__ = __str__

    @property
    def fully_verified(self):
        return self.verified and self.verification_document_verified

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
