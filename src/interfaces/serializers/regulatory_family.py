from rest_framework import serializers

from constants import help_text, choices
from data import RegulatoryFamily
from interfaces.serializers.base import BaseSerializer, URLField
from interfaces.serializers.relationships import (SourceRelationshipSerializer, RelationshipSerializer,
                                                  SourceField)


class RegulatoryFamilyListSerializer(BaseSerializer):
    model = RegulatoryFamily

    # properties
    name = serializers.CharField(required=True, max_length=250, help_text=help_text.required_name)
    mechanism = serializers.ChoiceField(required=False,
                                        choices=choices.mechanism,
                                        help_text=help_text.mechanism)

    # write-only
    rfam = serializers.CharField(required=False, write_only=True, max_length=100, help_text=help_text.rfam)
    description = serializers.CharField(required=False, write_only=True, help_text=help_text.generic_description)

    # url
    url = URLField(read_only=True,
                   view_name='rfams-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')


class RegulatoryFamilyDetailSerializer(RegulatoryFamilyListSerializer):
    url = None

    rfam = serializers.CharField(required=False, max_length=100, help_text=help_text.rfam)
    description = serializers.CharField(required=False, help_text=help_text.generic_description)

    # relationships
    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceField(read_only=True))
    regulator = RelationshipSerializer(read_only=True,
                                       child=serializers.HyperlinkedRelatedField(
                                           read_only=True,
                                           view_name='regulators-detail',
                                           lookup_field='protrend_id',
                                           lookup_url_kwarg='protrend_id'))
