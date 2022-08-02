from rest_framework import serializers

from constants import help_text, choices


class NestedField(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def get_attribute(self, instance):
        attribute = super(NestedField, self).get_attribute(instance)
        if isinstance(attribute, list) and attribute:
            return attribute[0]
        return attribute


# ----------------------------------------------------------
# URL Field
# ----------------------------------------------------------
class URLField(serializers.HyperlinkedIdentityField):

    # noinspection PyShadowingBuiltins
    def get_url(self, obj, view_name, request, format):
        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value}
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)


# ----------------------------------------------------------
# Source Field
# ----------------------------------------------------------
class SourceField(serializers.Serializer):
    # properties
    name = serializers.CharField(read_only=True, max_length=100, help_text=help_text.source_name)
    url = serializers.CharField(read_only=True, help_text=help_text.source_url)
    external_identifier = serializers.CharField(read_only=True, help_text=help_text.source_external_identifier)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        if hasattr(instance, 'relationship_'):
            url = getattr(instance.relationship_, 'url', None)
            if url:
                setattr(instance, 'url', url)

            external_id = getattr(instance.relationship_, 'external_identifier', None)
            if external_id:
                setattr(instance, 'external_identifier', external_id)
        return super(SourceField, self).to_representation(instance)


# ----------------------------------------------------------
# MotifTFBSField Field
# ----------------------------------------------------------
class MotifTFBSField(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    sequence = serializers.CharField(read_only=True, help_text=help_text.tfbs_sequence)
    strand = serializers.ChoiceField(read_only=True, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.stop)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        if hasattr(instance, 'relationship_'):

            for _field in ('sequence', 'strand', 'start', 'stop'):
                val = getattr(instance.relationship_, _field, None)
                if val:
                    setattr(instance, _field, val)

        return super(MotifTFBSField, self).to_representation(instance)
