import abc

from rest_framework import serializers

from constants import help_text, choices
from interfaces.serializers.effector import EffectorHighlightSerializer
from interfaces.serializers.gene import GeneHighlightSerializer
from interfaces.serializers.regulator import RegulatorHighlightSerializer
from interfaces.serializers.tfbs import TFBSHighlightSerializer


class TRNSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)

    # url
    url = serializers.HyperlinkedIdentityField(read_only=True,
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
    regulator = RegulatorHighlightSerializer(read_only=True)
    gene = GeneHighlightSerializer(read_only=True)
    tfbs = TFBSHighlightSerializer(read_only=True)
    effector = EffectorHighlightSerializer(read_only=True)

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass

    @abc.abstractmethod
    def delete(self, instance):
        pass