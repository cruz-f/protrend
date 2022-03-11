from rest_framework import serializers

from constants import help_text, choices
from data import TFBS
from interfaces.validation import validate_dna_sequence
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.fields import URLField, SourceField
from interfaces.serializers.relationship import SourceRelationshipSerializer, RelationshipSerializer
from interfaces.api.serializers.fields import OrganismField


class TFBSListSerializer(BaseSerializer):
    model = TFBS

    # properties
    organism = serializers.CharField(required=True, max_length=100, help_text=help_text.organism_id)
    sequence = serializers.CharField(required=True, help_text=help_text.tfbs_sequence)
    strand = serializers.ChoiceField(required=True, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, help_text=help_text.stop)
    length = serializers.IntegerField(required=True, min_value=0, help_text=help_text.length)

    # url
    url = URLField(read_only=True,
                   view_name='binding-sites-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')

    def validate(self, attrs):
        validated_data = validate_dna_sequence(attrs)
        return validated_data


class TFBSDetailSerializer(TFBSListSerializer):
    url = None
    organism = OrganismField(read_only=True, source='data_organism')

    # relationships
    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceField(read_only=True))
    evidence = RelationshipSerializer(read_only=True,
                                      child=serializers.HyperlinkedRelatedField(
                                          read_only=True,
                                          view_name='evidences-detail',
                                          lookup_field='protrend_id',
                                          lookup_url_kwarg='protrend_id'))
    publication = RelationshipSerializer(read_only=True,
                                         child=serializers.HyperlinkedRelatedField(
                                             read_only=True,
                                             view_name='publications-detail',
                                             lookup_field='protrend_id',
                                             lookup_url_kwarg='protrend_id'))
    data_organism = RelationshipSerializer(read_only=True,
                                           child=serializers.HyperlinkedRelatedField(
                                               read_only=True,
                                               view_name='organisms-detail',
                                               lookup_field='protrend_id',
                                               lookup_url_kwarg='protrend_id'))
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
    regulatory_interaction = RelationshipSerializer(read_only=True,
                                                    child=serializers.HyperlinkedRelatedField(
                                                        read_only=True,
                                                        view_name='interactions-detail',
                                                        lookup_field='protrend_id',
                                                        lookup_url_kwarg='protrend_id'))
