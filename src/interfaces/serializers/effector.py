import abc

from rest_framework import serializers, status

import domain.database as papi
from constants import help_text
from exceptions import ProtrendException
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.relationships import SourceRelationshipSerializer, SourceHighlightSerializer, \
    RelationshipSerializer


class EffectorSerializer(BaseSerializer):
    # properties
    name = serializers.CharField(required=True, max_length=250, help_text=help_text.required_name)
    kegg_compounds = serializers.ListField(child=serializers.CharField(required=False),
                                           required=False,
                                           help_text=help_text.kegg_compounds)

    # url
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='effectors-detail',
                                               lookup_field='protrend_id',
                                               lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        return papi.create_effector(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_effector(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_effector(instance)


class EffectorDetailSerializer(EffectorSerializer):
    url = None

    # relationships
    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceHighlightSerializer(read_only=True))
    regulator = RelationshipSerializer(read_only=True,
                                       child=serializers.HyperlinkedRelatedField(
                                           read_only=True,
                                           view_name='regulators-detail',
                                           lookup_field='protrend_id',
                                           lookup_url_kwarg='protrend_id'))
    regulatory_interaction = RelationshipSerializer(read_only=True,
                                                    child=serializers.HyperlinkedRelatedField(
                                                        read_only=True,
                                                        view_name='interactions-detail',
                                                        lookup_field='protrend_id',
                                                        lookup_url_kwarg='protrend_id'))


class EffectorHighlightSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    name = serializers.CharField(read_only=True, max_length=250, help_text=help_text.required_name)

    @abc.abstractmethod
    def create(self, validated_data):
        pass

    @abc.abstractmethod
    def update(self, instance, validated_data):
        pass

    def get_attribute(self, instance):
        if instance.effector is None:
            return

        effector = papi.get_effector_by_id(instance.effector)
        if effector is None:
            raise ProtrendException(detail=f'Effector with protrend id {instance.effector} not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)

        return effector
