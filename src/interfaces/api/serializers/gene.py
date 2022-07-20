from rest_framework import serializers

from constants import help_text, choices
from data.models import Gene
from interfaces.validation import validate_protein_sequence
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.fields import URLField, SourceField
from interfaces.serializers.relationship import SourceRelationshipSerializer, RelationshipSerializer


class GeneListSerializer(BaseSerializer):
    model = Gene

    # properties
    locus_tag = serializers.CharField(required=True, max_length=50, help_text=help_text.locus_tag)
    uniprot_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.uniprot_accession)
    name = serializers.CharField(required=False, max_length=50, help_text=help_text.gene_name)
    synonyms = serializers.ListField(required=False, child=serializers.CharField(required=False),
                                     help_text=help_text.synonyms)

    # write only
    function = serializers.CharField(required=False, write_only=True, help_text=help_text.function)
    description = serializers.CharField(required=False, write_only=True, help_text=help_text.description)
    ncbi_gene = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.ncbi_gene)
    ncbi_protein = serializers.IntegerField(required=False, min_value=0, write_only=True,
                                            help_text=help_text.ncbi_protein)
    genbank_accession = serializers.CharField(required=False, write_only=True, max_length=50,
                                              help_text=help_text.genbank_accession)
    refseq_accession = serializers.CharField(required=False, write_only=True, max_length=50,
                                             help_text=help_text.refseq_accession)
    sequence = serializers.CharField(required=False, write_only=True, help_text=help_text.sequence)
    strand = serializers.ChoiceField(required=False, write_only=True, choices=choices.strand,
                                     help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.stop)

    # url
    url = URLField(read_only=True,
                   view_name='genes-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')

    def validate(self, attrs):
        validated_data = validate_protein_sequence(attrs)
        return validated_data


class GeneDetailSerializer(GeneListSerializer):
    url = None

    # write only
    function = serializers.CharField(required=False, help_text=help_text.function)
    description = serializers.CharField(required=False, help_text=help_text.description)
    ncbi_gene = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_gene)
    ncbi_protein = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_protein)
    genbank_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.genbank_accession)
    refseq_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.refseq_accession)
    sequence = serializers.CharField(required=False, help_text=help_text.sequence)
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
    operon = RelationshipSerializer(read_only=True,
                                    child=serializers.HyperlinkedRelatedField(
                                        read_only=True,
                                        view_name='operons-detail',
                                        lookup_field='protrend_id',
                                        lookup_url_kwarg='protrend_id'))
    regulator = RelationshipSerializer(read_only=True,
                                       child=serializers.HyperlinkedRelatedField(
                                           read_only=True,
                                           view_name='regulators-detail',
                                           lookup_field='protrend_id',
                                           lookup_url_kwarg='protrend_id'))
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
