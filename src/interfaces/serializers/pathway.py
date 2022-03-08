from rest_framework import serializers

from constants import help_text
from data import Pathway
from interfaces.serializers.base import BaseSerializer, URLField
from interfaces.serializers.relationships import (SourceRelationshipSerializer, SourceField,
                                                  RelationshipSerializer)


class PathwayListSerializer(BaseSerializer):
    _data_model = Pathway

    # properties
    name = serializers.CharField(required=True, max_length=250, help_text=help_text.required_name)
    kegg_pathways = serializers.ListField(required=False, child=serializers.CharField(required=False),
                                          help_text=help_text.kegg_pathways)

    # url
    url = URLField(read_only=True,
                   view_name='pathways-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')


class PathwayDetailSerializer(PathwayListSerializer):
    url = None

    # relationships
    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceField(read_only=True))
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
