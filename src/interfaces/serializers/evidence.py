from rest_framework import serializers

import domain.database as papi
from constants import help_text
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.relationships import RelationshipSerializer


class EvidenceSerializer(BaseSerializer):
    # properties
    name = serializers.CharField(required=True, max_length=250, help_text=help_text.required_name)
    description = serializers.CharField(required=False, help_text=help_text.generic_description)

    # url
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='evidences-detail',
                                               lookup_field='protrend_id',
                                               lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        return papi.create_evidence(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_evidence(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_evidence(instance)


class EvidenceDetailSerializer(EvidenceSerializer):
    url = None

    # relationships
    tfbs = RelationshipSerializer(read_only=True,
                                  child=serializers.HyperlinkedRelatedField(
                                      read_only=True,
                                      view_name='binding-sites-detail',
                                      lookup_field='protrend_id',
                                      lookup_url_kwarg='protrend_id'))
    regulatory_interaction = RelationshipSerializer(read_only=True,
                                                    child=serializers.HyperlinkedRelatedField(
                                                        read_only=True,
                                                        view_name='interactions-detail',
                                                        lookup_field='protrend_id',
                                                        lookup_url_kwarg='protrend_id'))
