import abc

from rest_framework import serializers

from constants import help_text


# --------------------------------------
# Base Serializer
# --------------------------------------
class BaseSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass
