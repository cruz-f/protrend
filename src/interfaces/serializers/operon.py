from rest_framework import serializers

import domain.database as papi
from constants import help_text, choices
from interfaces.serializers.base import BaseSerializer, URLField
from interfaces.serializers.gene import GeneListSerializer, GeneHighlightSerializer
from interfaces.serializers.relationships import SourceRelationshipSerializer, SourceHighlightSerializer, \
    RelationshipSerializer
from interfaces.validation import validate_operon_genes


class OperonSerializer(BaseSerializer):
    # properties
    operon_db_id = serializers.CharField(required=True, max_length=50, help_text=help_text.operon_db_id)
    name = serializers.CharField(required=False, max_length=50, help_text=help_text.operon_name)
    function = serializers.CharField(required=False, max_length=250, help_text=help_text.operon_function)
    genes = serializers.ListField(required=True, child=serializers.CharField(required=True),
                                  help_text=help_text.operon_genes)
    strand = serializers.ChoiceField(required=False, write_only=True, choices=choices.strand,
                                     help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.stop)

    # url
    url = URLField(read_only=True,
                   view_name='operons-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        validate_operon_genes(validated_data)
        return papi.create_operon(**validated_data)

    def update(self, instance, validated_data):
        validate_operon_genes(validated_data, instance)
        return papi.update_operon(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_operon(instance)


class OperonDetailSerializer(OperonSerializer):
    url = None
    genes = GeneListSerializer(read_only=True,
                               child=GeneHighlightSerializer(read_only=True),
                               help_text=help_text.operon_genes)
    strand = serializers.ChoiceField(required=False, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, help_text=help_text.stop)

    # relationships
    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceHighlightSerializer(read_only=True))
    organism = RelationshipSerializer(read_only=True,
                                      child=serializers.HyperlinkedRelatedField(
                                          read_only=True,
                                          view_name='organisms-detail',
                                          lookup_field='protrend_id',
                                          lookup_url_kwarg='protrend_id'))
    gene = RelationshipSerializer(read_only=True,
                                  child=serializers.HyperlinkedRelatedField(
                                      read_only=True,
                                      view_name='genes-detail',
                                      lookup_field='protrend_id',
                                      lookup_url_kwarg='protrend_id'))
