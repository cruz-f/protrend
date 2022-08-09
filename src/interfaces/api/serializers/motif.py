from rest_framework import serializers

from constants import help_text
from interfaces.api.serializers.fields import TFBSField, RegulatorField
from interfaces.serializers.fields import URLField, MotifTFBSField
from interfaces.serializers.relationship import RelationshipSerializer


class MotifListSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    regulator = serializers.CharField(required=True, max_length=100, help_text=help_text.regulator_id)
    tfbs = serializers.ListField(required=True, child=serializers.CharField(required=True),
                                 help_text=help_text.tfbs_id)
    sequences = serializers.ListField(required=True, child=serializers.CharField(required=True),
                                      help_text=help_text.aligned_sequences)
    consensus_sequence = serializers.CharField(required=True, help_text=help_text.consensus_sequence)

    # url
    url = URLField(read_only=True,
                   view_name='motifs-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class MotifDetailSerializer(MotifListSerializer):
    url = None

    regulator = RegulatorField(read_only=True, source='data_regulator')
    tfbs = serializers.ListSerializer(read_only=True,
                                      source='data_tfbs',
                                      child=MotifTFBSField(read_only=True),
                                      help_text=help_text.tfbs_id)

    organism = RelationshipSerializer(read_only=True,
                                      child=serializers.HyperlinkedRelatedField(
                                          read_only=True,
                                          view_name='organisms-detail',
                                          lookup_field='protrend_id',
                                          lookup_url_kwarg='protrend_id'))
    data_regulator = RelationshipSerializer(read_only=True,
                                            child=serializers.HyperlinkedRelatedField(
                                                read_only=True,
                                                view_name='regulators-detail',
                                                lookup_field='protrend_id',
                                                lookup_url_kwarg='protrend_id'))
    data_tfbs = RelationshipSerializer(read_only=True,
                                       child=serializers.HyperlinkedRelatedField(
                                           read_only=True,
                                           view_name='binding-sites-detail',
                                           lookup_field='protrend_id',
                                           lookup_url_kwarg='protrend_id'))

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
