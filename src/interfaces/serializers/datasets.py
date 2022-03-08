import abc

from rest_framework import serializers

from constants import help_text, choices
from interfaces.serializers.base import URLField
from interfaces.serializers.effector import EffectorField
from interfaces.serializers.gene import GeneField
from interfaces.serializers.regulator import RegulatorField
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
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    regulatory_effect = serializers.ChoiceField(required=True, choices=choices.regulatory_effect,
                                                help_text=help_text.regulatory_effect)
    regulator = RegulatorField(read_only=True)
    gene = GeneField(read_only=True)
    tfbs = TFBSField(read_only=True)
    effector = EffectorField(read_only=True)

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
    sequence = serializers.CharField(read_only=True, help_text=help_text.tfbs_sequence)
    strand = serializers.ChoiceField(read_only=True, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.stop)

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
    regulator = RegulatorField(read_only=True)
    tfbs = TFBSField(read_only=True)

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass
