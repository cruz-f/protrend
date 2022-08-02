from rest_framework import serializers

from constants import help_text
from interfaces.api.serializers.fields import RegulatoryInteractionField
from interfaces.serializers.fields import URLField


class TRNListSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)

    # url
    url = URLField(read_only=True,
                   view_name='trns-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class TRNDetailSerializer(serializers.Serializer):
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    name = serializers.CharField(required=True, max_length=200, help_text=help_text.organism_name)
    ncbi_taxonomy = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_taxonomy)
    species = serializers.CharField(required=False, max_length=150, help_text=help_text.species)
    strain = serializers.CharField(required=False, max_length=150, help_text=help_text.strain)

    regulatory_interaction = serializers.ListSerializer(read_only=True,
                                                        child=RegulatoryInteractionField(read_only=True))

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
