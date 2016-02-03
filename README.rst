=============
Charity Check
=============

A charity validator for applications with donations.


Installation
============

`$ pip install django-charity-check`


Configuration
=============

To configure Charity Check you'll need to provide two parameters to the CHARITY_CHECK configuration block::

  CHARITY_CHECK = {
      "dbm_location": "/path/to/directory/owned/by/current/user",
      "charity_model": "myapp.Charity"  # defaults to settings.AUTH_USER_MODEL
  }


Validation
==========

Most of the dirty work of Charity Check involves downloading and formating a local dmb with an csv file from the IRS containing all valid non profit organizations. This downloading, parsing, and storing proceedure should be done a minimum of every 14 days ( to keep in the loop of oranizations which have recently lost their non-profit status ). As such a few celery tasks have been included in the project to aid this process. You will configure celery in your django settings to include::

  CELERY_BEAT_SCHEDULE = {
      "update_charities_dmb": {
          "task": "charity_check.tasks.get_dmb,
          "schedule": timedelta(days=7)
      },
      "recheck_charities": {
          "task": "charity_check.tasks.check_charities,
          "schedule": timedelta(days=7)
      }
  }

The schedule parameter of these periodic tasks can either be a `datetime.timedelta` or a `celery.schedules.crontab` instance.


Models
======

`CharityCheck(*ein, name, city, state, country, deductability_code, charity*)`
