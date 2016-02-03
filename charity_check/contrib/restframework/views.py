from rest_framework.viewsets import ModelViewSet

from charity_check import models
from . import permissions, serializers


class CharityCheckViewset(ModelViewSet):
    """
    """
    model = models.CharityCheck
    queryset = models.CharityCheck.objects.all()
    serializer_class = serializers.CharityCheckSerializer
    permission_classes = (permissions.CharityCheckPermission,)
