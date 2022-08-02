from rest_framework import serializers

from constants import help_text, choices
from data.models import RegulatoryInteraction
from interfaces.serializers.base import BaseSerializer
from interfaces.serializers.fields import SourceField
from interfaces.serializers.relationship import SourceRelationshipSerializer
from interfaces.website.serializers.fields import OrganismField, RegulatorField, GeneField, TFBSField, EffectorField, \
    EvidenceField, PublicationField


class RegulatoryInteractionSerializer(BaseSerializer):
    model = RegulatoryInteraction

    # properties
    organism = serializers.CharField(required=True, max_length=100, help_text=help_text.organism_id)
    regulator = serializers.CharField(required=True, max_length=100, help_text=help_text.regulator_id)
    gene = serializers.CharField(required=True, max_length=100, help_text=help_text.gene_id)
    tfbs = serializers.CharField(required=False, max_length=100, help_text=help_text.tfbs_id)
    effector = serializers.CharField(required=False, max_length=100, help_text=help_text.effector_id)
    regulatory_effect = serializers.ChoiceField(required=True, choices=choices.regulatory_effect,
                                                help_text=help_text.regulatory_effect)

    # relationships
    data_source = SourceRelationshipSerializer(read_only=True,
                                               child=SourceField(read_only=True))
    evidence = EvidenceField(read_only=True, many=True)
    publication = PublicationField(read_only=True, many=True)

    data_organism = OrganismField(read_only=True, many=True)
    data_regulator = RegulatorField(read_only=True, many=True)
    data_gene = GeneField(read_only=True, many=True)
    data_tfbs = TFBSField(read_only=True, many=True)
    data_effector = EffectorField(read_only=True, many=True)
