from rest_framework import serializers

from constants import help_text
from data import Effector
from interfaces.serializers.base import BaseSerializer, URLField, NestedField
from interfaces.serializers.relationships import (SourceRelationshipSerializer,
                                                  SourceField,
                                                  RelationshipSerializer)


class EffectorListSerializer(BaseSerializer):
    model = Effector

    # properties
    name = serializers.CharField(required=True, max_length=250, help_text=help_text.required_name)
    kegg_compounds = serializers.ListField(child=serializers.CharField(required=False), required=False,
                                           help_text=help_text.kegg_compounds)

    # url
    url = URLField(read_only=True,
                   view_name='effectors-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')


class EffectorDetailSerializer(EffectorListSerializer):
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
    regulatory_interaction = RelationshipSerializer(read_only=True,
                                                    child=serializers.HyperlinkedRelatedField(
                                                        read_only=True,
                                                        view_name='interactions-detail',
                                                        lookup_field='protrend_id',
                                                        lookup_url_kwarg='protrend_id'))


class EffectorField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    name = serializers.CharField(read_only=True, max_length=250, help_text=help_text.required_name)
