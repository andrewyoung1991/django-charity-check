import pytest
from model_mommy import mommy

from charity_check.models import verification_document_handler


@pytest.mark.django_db
def test_document_handler():
    instance = mommy.make("charity_check.CharityCheck")
    filename = "501(c)3.pdf"
    path = verification_document_handler(instance, filename)
    assert isinstance(path, str)
