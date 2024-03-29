from rest_framework import serializers

from constants import help_text
from data.models import Organism
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.fields import SourceField, URLField
from interfaces.serializers.relationship import RelationshipSerializer, SourceRelationshipSerializer


class OrganismListSerializer(BaseSerializer):
    model = Organism

    # properties
    name = serializers.CharField(required=True, max_length=200, help_text=help_text.organism_name)
    ncbi_taxonomy = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_taxonomy)
    species = serializers.CharField(required=False, max_length=150, help_text=help_text.species)
    strain = serializers.CharField(required=False, max_length=150, help_text=help_text.strain)

    # write-only
    refseq_accession = serializers.CharField(required=False, write_only=True, max_length=50,
                                             help_text=help_text.refseq_accession)
    refseq_ftp = serializers.CharField(required=False, write_only=True, max_length=250,
                                       help_text=help_text.refseq_ftp)
    genbank_accession = serializers.CharField(required=False, write_only=True, max_length=50,
                                              help_text=help_text.genbank_accession)
    genbank_ftp = serializers.CharField(required=False, write_only=True, max_length=250,
                                        help_text=help_text.genbank_ftp)
    ncbi_assembly = serializers.IntegerField(required=False, min_value=0, write_only=True,
                                             help_text=help_text.ncbi_assembly)
    assembly_accession = serializers.CharField(required=False, write_only=True, max_length=50,
                                               help_text=help_text.assembly_accession)

    # url
    url = URLField(read_only=True,
                   view_name='organisms-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')


class OrganismDetailSerializer(OrganismListSerializer):
    url = None
    refseq_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.refseq_accession)
    refseq_ftp = serializers.CharField(required=False, max_length=250, help_text=help_text.refseq_ftp)
    genbank_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.genbank_accession)
    genbank_ftp = serializers.CharField(required=False, max_length=250, help_text=help_text.genbank_ftp)
    ncbi_assembly = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_assembly)
    assembly_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.assembly_accession)

    # relationships
    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceField(read_only=True))
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
    motif = RelationshipSerializer(read_only=True,
                                   child=serializers.HyperlinkedRelatedField(
                                       read_only=True,
                                       view_name='motifs-detail',
                                       lookup_field='protrend_id',
                                       lookup_url_kwarg='protrend_id'))
