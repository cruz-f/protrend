from rest_framework import serializers

from constants import help_text
from data.models import Organism
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.fields import SourceField, URLField
from interfaces.serializers.relationship import SourceRelationshipSerializer
from interfaces.website.serializers.fields import (RegulatorField, GeneField, TFBSField,
                                                   RegulatoryInteractionField)


class OrganismsSerializer(BaseSerializer):
    model = Organism

    # properties
    name = serializers.CharField(required=True, max_length=200, help_text=help_text.organism_name)
    ncbi_taxonomy = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_taxonomy)
    strain = serializers.CharField(required=False, max_length=150, help_text=help_text.strain)
    refseq_accession = serializers.CharField(required=False, max_length=50,
                                             help_text=help_text.refseq_accession)
    genbank_accession = serializers.CharField(required=False, max_length=50,
                                              help_text=help_text.genbank_accession)
    assembly_accession = serializers.CharField(required=False, max_length=50,
                                               help_text=help_text.assembly_accession)

    url = URLField(read_only=True,
                   view_name='organism',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')


class OrganismSerializer(OrganismsSerializer):
    url = None

    species = serializers.CharField(required=False, max_length=150, help_text=help_text.species)
    refseq_ftp = serializers.CharField(required=False, max_length=250, help_text=help_text.refseq_ftp)
    genbank_ftp = serializers.CharField(required=False, max_length=250, help_text=help_text.genbank_ftp)
    ncbi_assembly = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_assembly)

    regulator = RegulatorField(read_only=True, many=True)
    gene = GeneField(read_only=True, many=True)
    tfbs = TFBSField(read_only=True, many=True)
    regulatory_interaction = RegulatoryInteractionField(read_only=True, many=True)

    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceField(read_only=True))


