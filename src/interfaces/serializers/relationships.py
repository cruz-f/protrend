import abc

from rest_framework import serializers

import domain.model_api as mapi
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

    def get_attribute(self, instance):
        return mapi.get_related_objects(instance, self.field_name)


class SourceRelationshipSerializer(RelationshipSerializer):

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass

    def get_attribute(self, instance):
        sources = super(SourceRelationshipSerializer, self).get_attribute(instance)
        relationships = []
        for source in sources:
            source_relationships = mapi.get_relationships(source=instance, rel='data_source', target=source)
            for source_rel in source_relationships:
                source_rel.name = source.name
                relationships.append(source_rel)
        return relationships


class SourceHighlightSerializer(serializers.Serializer):
    # properties
    name = serializers.CharField(read_only=True, max_length=100, help_text=help_text.required_name)
    url = serializers.CharField(read_only=True, help_text=help_text.url)

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass
