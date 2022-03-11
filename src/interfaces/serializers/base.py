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

    def create(self, validated_data):
        return dpi.create_objects(cls=self.model, values=(validated_data,))

    def update(self, instance, validated_data):
        return dpi.update_objects((instance,), (validated_data,))

    # noinspection PyMethodMayBeStatic
    def delete(self, instance):
        return dpi.delete_objects((instance,))
