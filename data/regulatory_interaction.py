from neomodel import StringProperty, RelationshipTo, One

from .base import BaseNode
from .relationships import REL_TYPE, SourceRelationship
from .utils import help_text, choices, default


class RegulatoryInteraction(BaseNode):
    entity = 'RIN'

    # properties
    regulatory_interaction_hash = StringProperty(required=True, max_length=600)
    organism = StringProperty(required=True, max_length=100, help_text=help_text.organism_id)
    regulator = StringProperty(required=True, max_length=100, help_text=help_text.regulator_id)
    gene = StringProperty(required=True, max_length=100, help_text=help_text.gene_id)
    tfbs = StringProperty(max_length=100, help_text=help_text.tfbs_id)
    effector = StringProperty(max_length=100, help_text=help_text.effector_id)
    regulatory_effect = StringProperty(required=True, choices=choices.regulatory_effect,
                                       default=default.regulatory_effect, max_length=50,
                                       help_text=help_text.regulatory_effect)

    # relationships
    data_source = RelationshipTo('.source.Source', REL_TYPE, model=SourceRelationship)
    evidence = RelationshipTo('.evidence.Evidence', REL_TYPE)
    publication = RelationshipTo('.publication.Publication', REL_TYPE)
    data_effector = RelationshipTo('.effector.Effector', REL_TYPE, cardinality=One)
    data_organism = RelationshipTo('organism.Organism', REL_TYPE, cardinality=One)
    data_regulator = RelationshipTo('.regulator.Regulator', REL_TYPE, cardinality=One)
    data_gene = RelationshipTo('.gene.Gene', REL_TYPE, cardinality=One)
    data_tfbs = RelationshipTo('.tfbs.TFBS', REL_TYPE, cardinality=One)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'organism', 'regulator', 'gene', 'tfbs', 'effector',
                  'regulatory_effect',
                  'data_source', 'evidence', 'publication', 'data_effector', 'data_organism', 'data_regulator',
                  'data_gene', 'data_tfbs']
