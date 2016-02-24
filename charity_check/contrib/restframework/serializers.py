from rest_framework import serializers

from charity_check import models


class CharityCheckSerializer(serializers.ModelSerializer):
    """
    """
    verification_failure_messages = \
        serializers.SerializerMethodField("get_failure_messages")
    verification_status = serializers.SerializerMethodField("get_verification_status")

    class Meta:
        model = models.CharityCheck
        read_only_fields = ("id", "charity", "verified", "verification_document_verified",
            "sanitized", "datetime_checked", "verification_status",
            "verification_failure_messages")

    def get_failure_message(self, instance):
        return instance.exceptions.values_list("message", flat=True)

    def get_verification_status(self, instance):
        return instance.get_verification_status_display()
