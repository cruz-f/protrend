from rest_framework import serializers

from constants import help_text, choices
from data import RegulatoryInteraction
from interfaces.serializers.base import BaseSerializer, URLField, NestedField
from interfaces.serializers.effector import EffectorField
from interfaces.serializers.gene import GeneField
from interfaces.serializers.organism import OrganismField
from interfaces.serializers.regulator import RegulatorField
from interfaces.serializers.relationships import (SourceRelationshipSerializer, SourceField,
                                                  RelationshipSerializer)
from interfaces.serializers.tfbs import TFBSField


class RegulatoryInteractionListSerializer(BaseSerializer):
    model = RegulatoryInteraction

    # properties
    organism = serializers.CharField(required=True, max_length=100, help_text=help_text.organism_id)
    regulator = serializers.CharField(required=True, max_length=100, help_text=help_text.regulator_id)
    gene = serializers.CharField(required=True, max_length=100, help_text=help_text.gene_id)
    tfbs = serializers.CharField(required=False, max_length=100, help_text=help_text.tfbs_id)
    effector = serializers.CharField(required=False, max_length=100, help_text=help_text.effector_id)
    regulatory_effect = serializers.ChoiceField(required=True, choices=choices.regulatory_effect,
                                                help_text=help_text.regulatory_effect)

    # url
    url = URLField(read_only=True,
                   view_name='interactions-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')


class RegulatoryInteractionDetailSerializer(RegulatoryInteractionListSerializer):
    url = None

    organism = OrganismField(read_only=True, source='data_organism')
    regulator = RegulatorField(read_only=True, source='data_regulator')
    gene = GeneField(read_only=True, source='data_gene')
    tfbs = TFBSField(read_only=True, source='data_tfbs')
    effector = EffectorField(read_only=True, source='data_effector')

    # relationships
    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceField(read_only=True))
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


class RegulatoryInteractionField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    regulator = serializers.CharField(required=True, max_length=100, help_text=help_text.regulator_id)
    gene = serializers.CharField(required=True, max_length=100, help_text=help_text.gene_id)
    tfbs = serializers.CharField(required=False, max_length=100, help_text=help_text.tfbs_id)
    effector = serializers.CharField(required=False, max_length=100, help_text=help_text.effector_id)
    regulatory_effect = serializers.ChoiceField(required=True, choices=choices.regulatory_effect,
                                                help_text=help_text.regulatory_effect)
