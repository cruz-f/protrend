from rest_framework import serializers, status

import domain.database as papi
from constants import help_text, choices
from exceptions import ProtrendException
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.organism import OrganismHighlightSerializer
from interfaces.serializers.relationships import SourceRelationshipSerializer, SourceHighlightSerializer, \
    RelationshipSerializer
from interfaces.validation import validate_dna_sequence


class TFBSSerializer(BaseSerializer):
    # properties
    organism = serializers.CharField(required=True, max_length=100, help_text=help_text.organism_id)
    sequence = serializers.CharField(required=True, help_text=help_text.tfbs_sequence)
    strand = serializers.ChoiceField(required=True, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, help_text=help_text.stop)
    length = serializers.IntegerField(required=True, min_value=0, help_text=help_text.length)

    # url
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='binding-sites-detail',
                                               lookup_field='protrend_id',
                                               lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        validated_data = validate_dna_sequence(validated_data)
        return papi.create_binding_site(**validated_data)

    def update(self, instance, validated_data):
        validated_data = validate_dna_sequence(validated_data, instance)
        return papi.update_binding_site(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_binding_site(instance)


class TFBSDetailSerializer(TFBSSerializer):
    url = None
    organism = OrganismHighlightSerializer(read_only=True)

    # relationships
    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceHighlightSerializer(read_only=True))
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


class TFBSHighlightSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    sequence = serializers.CharField(read_only=True, help_text=help_text.tfbs_sequence)
    strand = serializers.ChoiceField(read_only=True, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.stop)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_attribute(self, instance):
        tfbs = papi.get_binding_site_by_id(instance.tfbs)
        if tfbs is None:
            raise ProtrendException(detail=f'TFBS with protrend id {instance.tfbs} not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)

        return tfbs
