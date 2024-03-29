from rest_framework import serializers

from constants import help_text, choices
from data.models import Regulator
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.fields import URLField, SourceField
from interfaces.serializers.relationship import SourceRelationshipSerializer
from interfaces.website.serializers.fields import (OrganismField, EffectorField, GeneField, TFBSField,
                                                   RegulatoryInteractionField, RegulatoryFamilyField, PathwayField,
                                                   MotifField)


class RegulatorsSerializer(BaseSerializer):
    model = Regulator

    # properties
    locus_tag = serializers.CharField(required=True, max_length=50, help_text=help_text.locus_tag)
    name = serializers.CharField(required=False, max_length=50, help_text=help_text.gene_name)
    mechanism = serializers.ChoiceField(required=False, choices=choices.mechanism,
                                        help_text=help_text.mechanism)
    uniprot_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.uniprot_accession)
    ncbi_gene = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_gene)
    ncbi_protein = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_protein)
    genbank_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.genbank_accession)
    refseq_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.refseq_accession)

    url = URLField(read_only=True,
                   view_name='regulator',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')


class RegulatorSerializer(RegulatorsSerializer):
    url = None

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
    effector = EffectorField(read_only=True, many=True)
    pathway = PathwayField(read_only=True, many=True)
    gene = GeneField(read_only=True, many=True)
    tfbs = TFBSField(read_only=True, many=True)
    regulatory_interaction = RegulatoryInteractionField(read_only=True, many=True)
    regulatory_family = RegulatoryFamilyField(read_only=True, many=True)
    motif = MotifField(read_only=True, many=True)

    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceField(read_only=True))
