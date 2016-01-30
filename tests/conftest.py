from django.conf import settings

import pytest
from model_mommy import mommy


@pytest.fixture
def charity(request):
    charity = mommy.make(settings.AUTH_USER_MODEL)
    def fin():
        charity.delete()
    return charity
