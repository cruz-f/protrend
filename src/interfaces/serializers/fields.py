import abc

from rest_framework import serializers

from constants import help_text


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
    name = serializers.CharField(read_only=True, max_length=100, help_text=help_text.required_name)
    url = serializers.CharField(read_only=True, help_text=help_text.url)
    external_identifier = serializers.CharField(read_only=True, help_text=help_text.url)

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
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
