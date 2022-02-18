from rest_framework import serializers

import domain.database as papi
from constants import help_text
from interfaces.serializers.base import BaseSerializer, URLField
from interfaces.serializers.relationships import SourceRelationshipSerializer, SourceHighlightSerializer, \
    RelationshipSerializer


class PathwaySerializer(BaseSerializer):
    # properties
    name = serializers.CharField(required=True, max_length=250, help_text=help_text.required_name)
    kegg_pathways = serializers.ListField(required=False,
                                          child=serializers.CharField(required=False),
                                          help_text=help_text.kegg_pathways)

    # url
    url = URLField(read_only=True,
                   view_name='pathways-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        return papi.create_pathway(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_pathway(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_pathway(instance)


class PathwayDetailSerializer(PathwaySerializer):
    url = None

    # relationships
    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceHighlightSerializer(read_only=True))
    regulator = RelationshipSerializer(read_only=True,
                                       child=serializers.HyperlinkedRelatedField(
                                           read_only=True,
                                           view_name='regulators-detail',
                                           lookup_field='protrend_id',
                                           lookup_url_kwarg='protrend_id'))
    gene = RelationshipSerializer(read_only=True,
                                  child=serializers.HyperlinkedRelatedField(
                                      read_only=True,
                                      view_name='genes-detail',
                                      lookup_field='protrend_id',
                                      lookup_url_kwarg='protrend_id'))
