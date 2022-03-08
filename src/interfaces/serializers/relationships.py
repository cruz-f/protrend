import abc

from rest_framework import serializers

from constants import help_text


# --------------------------------------
# Relationship Serializers
# --------------------------------------
class RelationshipSerializer(serializers.ListSerializer):

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass


class SourceRelationshipSerializer(RelationshipSerializer):

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass


class SourceField(serializers.Serializer):
    # properties
    name = serializers.CharField(read_only=True, max_length=100, help_text=help_text.required_name)
    url = serializers.CharField(read_only=True, help_text=help_text.url)

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass
