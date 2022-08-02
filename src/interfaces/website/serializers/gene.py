from rest_framework import serializers

from constants import help_text, choices
from data.models import Gene
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.fields import SourceField
from interfaces.serializers.relationship import SourceRelationshipSerializer
from interfaces.website.serializers.fields import OrganismField, OperonField


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
    gene_sequence = serializers.CharField(required=False, help_text=help_text.gene_sequence)
    protein_sequence = serializers.CharField(required=False, help_text=help_text.protein_sequence)
    strand = serializers.ChoiceField(required=False, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, help_text=help_text.stop)

    # relationships
    organism = OrganismField(read_only=True, many=True)
    operon = OperonField(read_only=True, many=True)

    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceField(read_only=True))
