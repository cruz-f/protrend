from neomodel import StringProperty, RelationshipTo

from constants import help_text
from .base import BaseNode
from .relationships import BASE_REL_TYPE, BaseRelationship


class Evidence(BaseNode):
    # properties
    name = StringProperty(required=True, unique_index=True, max_length=250, help_text=help_text.evidence_name)
    name_factor = StringProperty(required=True, unique_index=True, max_length=250, help_text=help_text.evidence_name)
    description = StringProperty(help_text=help_text.evidence_description)

    # relationships
    regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    operon = RelationshipTo('.operon.Operon', BASE_REL_TYPE, model=BaseRelationship)
    gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)
    tfbs = RelationshipTo('.tfbs.TFBS', BASE_REL_TYPE, model=BaseRelationship)
    regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', BASE_REL_TYPE,
                                            model=BaseRelationship)
