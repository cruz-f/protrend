from rest_framework import serializers

from constants import help_text
from data import Evidence
from interfaces.serializers.base import BaseSerializer, URLField
from interfaces.serializers.relationships import RelationshipSerializer


class EvidenceListSerializer(BaseSerializer):
    _data_model = Evidence

    # properties
    name = serializers.CharField(required=True, max_length=250, help_text=help_text.required_name)
    description = serializers.CharField(required=False, help_text=help_text.generic_description)

    # url
    url = URLField(read_only=True,
                   view_name='evidences-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')


class EvidenceDetailSerializer(EvidenceListSerializer):
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
