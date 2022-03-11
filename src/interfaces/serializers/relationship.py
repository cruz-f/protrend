import abc

from rest_framework import serializers


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
