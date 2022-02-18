from rest_framework import serializers

import domain.database as papi
from constants import help_text, choices
from interfaces.serializers.base import BaseSerializer, URLField
from interfaces.serializers.relationships import SourceRelationshipSerializer, RelationshipSerializer, \
    SourceHighlightSerializer


class RegulatoryFamilySerializer(BaseSerializer):
    # properties
    name = serializers.CharField(required=True, max_length=250, help_text=help_text.required_name)
    mechanism = serializers.ChoiceField(required=False,
                                        choices=choices.mechanism,
                                        help_text=help_text.mechanism)
    rfam = serializers.CharField(required=False, write_only=True, max_length=100, help_text=help_text.rfam)
    description = serializers.CharField(required=False, write_only=True, help_text=help_text.generic_description)

    # url
    url = URLField(read_only=True,
                   view_name='rfams-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        return papi.create_rfam(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_rfam(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_rfam(instance)


class RegulatoryFamilyDetailSerializer(RegulatoryFamilySerializer):
    url = None
    rfam = serializers.CharField(required=False, max_length=100, help_text=help_text.rfam)
    description = serializers.CharField(required=False, help_text=help_text.generic_description)

    # relationships
    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceHighlightSerializer(read_only=True))
    regulator = RelationshipSerializer(read_only=True,
                                       child=serializers.HyperlinkedRelatedField(
                                           read_only=True,
                                           view_name='regulators-detail',
                                           lookup_field='protrend_id',
                                           lookup_url_kwarg='protrend_id'))
