from rest_framework import serializers

from constants import help_text, choices
from data.models import Operon
from interfaces.api.serializers.fields import GeneField
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.fields import URLField, SourceField
from interfaces.serializers.relationship import SourceRelationshipSerializer, RelationshipSerializer


class OperonListSerializer(BaseSerializer):
    model = Operon

    # properties
    operon_db_id = serializers.CharField(required=True, max_length=50, help_text=help_text.operon_db_id)
    name = serializers.CharField(required=False, max_length=50, help_text=help_text.operon_name)
    function = serializers.CharField(required=False, max_length=250, help_text=help_text.operon_function)
    genes = serializers.ListField(required=True, child=serializers.CharField(required=True),
                                  help_text=help_text.operon_genes)

    # write only
    strand = serializers.ChoiceField(required=False, write_only=True, choices=choices.strand,
                                     help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.stop)

    # url
    url = URLField(read_only=True,
                   view_name='operons-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')


class OperonDetailSerializer(OperonListSerializer):
    url = None

    genes = serializers.ListSerializer(read_only=True,
                                       source='gene',
                                       child=GeneField(read_only=True),
                                       help_text=help_text.operon_genes)
    strand = serializers.ChoiceField(required=False, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, help_text=help_text.stop)

    # relationships
    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceField(read_only=True))
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
