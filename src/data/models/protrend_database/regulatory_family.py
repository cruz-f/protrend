from neomodel import StringProperty, RelationshipTo

from .base import BaseNode
from .relationships import BASE_REL_TYPE, SourceRelationship, BaseRelationship, SOURCE_REL_TYPE
from constants import help_text, choices


class RegulatoryFamily(BaseNode):
    # properties
    name = StringProperty(required=True, unique_index=True, max_length=250, help_text=help_text.rfam_name)
    name_factor = StringProperty(required=True, unique_index=True, max_length=250, help_text=help_text.rfam_name)
    mechanism = StringProperty(required=True, choices=choices.mechanism,
                               help_text=help_text.mechanism)
    rfam = StringProperty(max_length=100, help_text=help_text.rfam)
    description = StringProperty(help_text=help_text.rfam_description)

    # relationships
    data_source = RelationshipTo('.source.Source', SOURCE_REL_TYPE, model=SourceRelationship)
    publication = RelationshipTo('.publication.Publication', BASE_REL_TYPE, model=BaseRelationship)
    regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
