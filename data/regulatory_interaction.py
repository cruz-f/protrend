from neomodel import StringProperty, RelationshipTo, One

from .base import BaseNode
from .relationships import BASE_REL_TYPE, SourceRelationship, BaseRelationship, SOURCE_REL_TYPE
from constants import help_text, choices


class RegulatoryInteraction(BaseNode):
    # properties
    regulatory_interaction_hash = StringProperty(required=True, unique_index=True, max_length=600)
    organism = StringProperty(required=True, max_length=100, help_text=help_text.organism_id)
    regulator = StringProperty(required=True, max_length=100, help_text=help_text.regulator_id)
    gene = StringProperty(required=True, max_length=100, help_text=help_text.gene_id)
    tfbs = StringProperty(max_length=100, help_text=help_text.tfbs_id)
    effector = StringProperty(max_length=100, help_text=help_text.effector_id)
    regulatory_effect = StringProperty(required=True, choices=choices.regulatory_effect,
                                       help_text=help_text.regulatory_effect)

    # relationships
    data_source = RelationshipTo('.source.Source', SOURCE_REL_TYPE, model=SourceRelationship)
    evidence = RelationshipTo('.evidence.Evidence', BASE_REL_TYPE, model=BaseRelationship)
    publication = RelationshipTo('.publication.Publication', BASE_REL_TYPE, model=BaseRelationship)
    data_effector = RelationshipTo('.effector.Effector', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    data_organism = RelationshipTo('.organism.Organism', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    data_regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    data_gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    data_tfbs = RelationshipTo('.tfbs.TFBS', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'organism', 'regulator', 'gene', 'tfbs', 'effector',
                  'regulatory_effect',
                  'data_source', 'evidence', 'publication', 'data_effector', 'data_organism', 'data_regulator',
                  'data_gene', 'data_tfbs']
