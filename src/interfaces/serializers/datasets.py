import abc

from rest_framework import serializers

from constants import help_text, choices
from interfaces.serializers.base import URLField
from interfaces.serializers.regulatory_interaction import RegulatoryInteractionField
from interfaces.serializers.tfbs import TFBSField


class TRNListSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)

    # url
    url = URLField(read_only=True,
                   view_name='trns-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass

    @abc.abstractmethod
    def delete(self, instance):
        pass


class TRNDetailSerializer(serializers.Serializer):
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    name = serializers.CharField(required=True, max_length=200, help_text=help_text.organism_name)
    ncbi_taxonomy = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_taxonomy)
    species = serializers.CharField(required=False, max_length=150, help_text=help_text.species)
    strain = serializers.CharField(required=False, max_length=150, help_text=help_text.strain)

    regulatory_interaction = serializers.ListSerializer(read_only=True,
                                                        child=RegulatoryInteractionField(read_only=True))

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass

    @abc.abstractmethod
    def delete(self, instance):
        pass


class OrganismBindingSitesListSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)

    # url
    url = URLField(read_only=True,
                   view_name='organisms-binding-sites-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass

    @abc.abstractmethod
    def delete(self, instance):
        pass


class OrganismBindingSitesDetailSerializer(serializers.Serializer):
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    name = serializers.CharField(required=True, max_length=200, help_text=help_text.organism_name)
    ncbi_taxonomy = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_taxonomy)
    species = serializers.CharField(required=False, max_length=150, help_text=help_text.species)
    strain = serializers.CharField(required=False, max_length=150, help_text=help_text.strain)

    tfbs = serializers.ListSerializer(read_only=True, child=TFBSField(read_only=True))

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass


class RegulatorBindingSitesListSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)

    # url
    url = URLField(read_only=True,
                   view_name='regulators-binding-sites-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass

    @abc.abstractmethod
    def delete(self, instance):
        pass


class RegulatorBindingSitesDetailSerializer(serializers.Serializer):
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    locus_tag = serializers.CharField(read_only=True, max_length=50, help_text=help_text.locus_tag)
    uniprot_accession = serializers.CharField(read_only=True, max_length=50, help_text=help_text.uniprot_accession)
    name = serializers.CharField(read_only=True, max_length=50, help_text=help_text.gene_name)
    mechanism = serializers.ChoiceField(read_only=True, choices=choices.mechanism,
                                        help_text=help_text.mechanism)

    tfbs = serializers.ListSerializer(read_only=True, child=TFBSField(read_only=True))

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass
