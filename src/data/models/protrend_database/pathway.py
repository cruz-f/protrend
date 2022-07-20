from neomodel import ArrayProperty, StringProperty, RelationshipTo

from .base import BaseNode
from .relationships import BASE_REL_TYPE, SourceRelationship, BaseRelationship, SOURCE_REL_TYPE
from constants import help_text


class Pathway(BaseNode):
    # properties
    name = StringProperty(required=True, unique_index=True, max_length=250, help_text=help_text.required_name)
    name_factor = StringProperty(required=True, unique_index=True, max_length=250, help_text=help_text.required_name)
    kegg_pathways = ArrayProperty(StringProperty(), help_text=help_text.kegg_pathways)

    # relationships
    data_source = RelationshipTo('.source.Source', SOURCE_REL_TYPE, model=SourceRelationship)
    regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)
