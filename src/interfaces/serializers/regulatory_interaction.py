from rest_framework import serializers

import domain.database as papi
from constants import help_text, choices
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.effector import EffectorHighlightSerializer
from interfaces.serializers.gene import GeneHighlightSerializer
from interfaces.serializers.organism import OrganismHighlightSerializer
from interfaces.serializers.regulator import RegulatorHighlightSerializer
from interfaces.serializers.relationships import SourceRelationshipSerializer, SourceHighlightSerializer, \
    RelationshipSerializer
from interfaces.serializers.tfbs import TFBSHighlightSerializer


class RegulatoryInteractionSerializer(BaseSerializer):
    # properties
    organism = serializers.CharField(required=True, max_length=100, help_text=help_text.organism_id)
    regulator = serializers.CharField(required=True, max_length=100, help_text=help_text.regulator_id)
    gene = serializers.CharField(required=True, max_length=100, help_text=help_text.gene_id)
    tfbs = serializers.CharField(required=False, max_length=100, help_text=help_text.tfbs_id)
    effector = serializers.CharField(required=False, max_length=100, help_text=help_text.effector_id)
    regulatory_effect = serializers.ChoiceField(required=True, choices=choices.regulatory_effect,
                                                help_text=help_text.regulatory_effect)

    # url
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='interactions-detail',
                                               lookup_field='protrend_id',
                                               lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        return papi.create_interaction(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_interaction(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_interaction(instance)


class RegulatoryInteractionDetailSerializer(RegulatoryInteractionSerializer):
    url = None
    organism = OrganismHighlightSerializer(read_only=True)
    regulator = RegulatorHighlightSerializer(read_only=True)
    gene = GeneHighlightSerializer(read_only=True)
    tfbs = TFBSHighlightSerializer(read_only=True)
    effector = EffectorHighlightSerializer(read_only=True)

    # relationships
    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceHighlightSerializer(read_only=True))
    evidence = RelationshipSerializer(read_only=True,
                                      child=serializers.HyperlinkedRelatedField(
                                          read_only=True,
                                          view_name='evidences-detail',
                                          lookup_field='protrend_id',
                                          lookup_url_kwarg='protrend_id'))
    publication = RelationshipSerializer(read_only=True,
                                         child=serializers.HyperlinkedRelatedField(
                                             read_only=True,
                                             view_name='publications-detail',
                                             lookup_field='protrend_id',
                                             lookup_url_kwarg='protrend_id'))
    data_organism = RelationshipSerializer(read_only=True,
                                           child=serializers.HyperlinkedRelatedField(
                                               read_only=True,
                                               view_name='organisms-detail',
                                               lookup_field='protrend_id',
                                               lookup_url_kwarg='protrend_id'))
    data_effector = RelationshipSerializer(read_only=True,
                                           child=serializers.HyperlinkedRelatedField(
                                               read_only=True,
                                               view_name='effectors-detail',
                                               lookup_field='protrend_id',
                                               lookup_url_kwarg='protrend_id'))
    data_regulator = RelationshipSerializer(read_only=True,
                                            child=serializers.HyperlinkedRelatedField(
                                                read_only=True,
                                                view_name='regulators-detail',
                                                lookup_field='protrend_id',
                                                lookup_url_kwarg='protrend_id'))
    data_gene = RelationshipSerializer(read_only=True,
                                       child=serializers.HyperlinkedRelatedField(
                                           read_only=True,
                                           view_name='genes-detail',
                                           lookup_field='protrend_id',
                                           lookup_url_kwarg='protrend_id'))
    data_tfbs = RelationshipSerializer(read_only=True,
                                       child=serializers.HyperlinkedRelatedField(
                                           read_only=True,
                                           view_name='binding-sites-detail',
                                           lookup_field='protrend_id',
                                           lookup_url_kwarg='protrend_id'))
