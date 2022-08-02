from neomodel import ArrayProperty, StringProperty, RelationshipTo

from .base import BaseNode
from .relationships import BASE_REL_TYPE, SourceRelationship, BaseRelationship, SOURCE_REL_TYPE
from constants import help_text


class Effector(BaseNode):
    # properties
    name = StringProperty(required=True, unique_index=True, max_length=250, help_text=help_text.effector_name)
    name_factor = StringProperty(required=True, unique_index=True, max_length=250, help_text=help_text.effector_name)
    kegg_compounds = ArrayProperty(StringProperty(), help_text=help_text.kegg_compounds)

    # relationships
    data_source = RelationshipTo('.source.Source', SOURCE_REL_TYPE, model=SourceRelationship)
    regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', BASE_REL_TYPE,
                                            model=BaseRelationship)
