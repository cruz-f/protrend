from rest_framework import serializers

from constants import help_text, choices
from data.models import Gene
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.fields import URLField, SourceField
from interfaces.serializers.relationship import SourceRelationshipSerializer
from interfaces.website.serializers.fields import (OrganismField, TFBSField,
                                                   RegulatoryInteractionField, RegulatorField)


class GeneSerializer(BaseSerializer):
    model = Gene

    # properties
    locus_tag = serializers.CharField(required=True, max_length=50, help_text=help_text.locus_tag)
    name = serializers.CharField(required=False, max_length=50, help_text=help_text.gene_name)
    uniprot_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.uniprot_accession)
    ncbi_gene = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_gene)
    ncbi_protein = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_protein)
    genbank_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.genbank_accession)
    refseq_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.refseq_accession)

    synonyms = serializers.ListField(required=False,
                                     child=serializers.CharField(required=False),
                                     help_text=help_text.synonyms)
    function = serializers.CharField(required=False, help_text=help_text.function)
    description = serializers.CharField(required=False, help_text=help_text.description)
    sequence = serializers.CharField(required=False, help_text=help_text.sequence)
    strand = serializers.ChoiceField(required=False, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, help_text=help_text.stop)

    url = URLField(read_only=True,
                   view_name='gene',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')

    # relationships
    organism = OrganismField(read_only=True, many=True)
    regulator = RegulatorField(read_only=True, many=True)
    tfbs = TFBSField(read_only=True, many=True)
    regulatory_interaction = RegulatoryInteractionField(read_only=True, many=True)

    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceField(read_only=True))
