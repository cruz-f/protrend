import abc

from rest_framework import serializers, status

import domain.database as papi
from constants import help_text, choices
from exceptions import ProtrendException
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.relationships import SourceRelationshipSerializer, SourceHighlightSerializer, \
    RelationshipSerializer
from interfaces.validation import validate_protein_sequence


class GeneSerializer(BaseSerializer):
    # properties
    locus_tag = serializers.CharField(required=True, max_length=50, help_text=help_text.locus_tag)
    uniprot_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.uniprot_accession)
    name = serializers.CharField(required=False, max_length=50, help_text=help_text.gene_name)
    synonyms = serializers.ListField(required=False,
                                     child=serializers.CharField(required=False),
                                     help_text=help_text.synonyms)
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
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='genes-detail',
                                               lookup_field='protrend_id',
                                               lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        validated_data = validate_protein_sequence(validated_data)
        return papi.create_gene(**validated_data)

    def update(self, instance, validated_data):
        validated_data = validate_protein_sequence(validated_data, instance)
        return papi.update_gene(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_gene(instance)


class GeneDetailSerializer(GeneSerializer):
    url = None
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
                                               child=SourceHighlightSerializer(read_only=True))
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


class GeneHighlightSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    locus_tag = serializers.CharField(read_only=True, max_length=50, help_text=help_text.locus_tag)
    uniprot_accession = serializers.CharField(read_only=True, max_length=50, help_text=help_text.uniprot_accession)
    name = serializers.CharField(read_only=True, max_length=50, help_text=help_text.gene_name)

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass

    def get_attribute(self, instance):
        gene = papi.get_gene_by_id(instance.gene)
        if gene is None:
            raise ProtrendException(detail=f'Gene with protrend id {instance.gene} not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)

        return gene


class GeneListSerializer(serializers.ListSerializer):

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass

    def get_attribute(self, instance):
        genes = []
        for gene_id in instance.genes:
            gene = papi.get_gene_by_id(gene_id)
            if gene is None:
                raise ProtrendException(detail=f'Gene with protrend id {gene_id} not found',
                                        code='get error',
                                        status=status.HTTP_404_NOT_FOUND)

            genes.append(gene)

        return genes