from rest_framework.permissions import BasePermission

from charity_check import CHARITY_CHECK


class CharityCheckPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        relation = getattr(obj.charity, CHARITY_CHECK["user_charity_relation"])
        return request.user.id == relation
