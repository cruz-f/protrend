from rest_framework import serializers

from constants import help_text
from domain import dpi


# --------------------------------------
# Base Serializer
# --------------------------------------
class BaseSerializer(serializers.Serializer):
    model = None

    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
