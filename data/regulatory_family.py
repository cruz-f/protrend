from neomodel import StringProperty, RelationshipTo

from .base import BaseNode, NameMixIn
from .relationships import REL_TYPE, SourceRelationship, BaseRelationship
from constants import help_text, choices


class RegulatoryFamily(BaseNode, NameMixIn):
    # properties
    mechanism = StringProperty(required=True, choices=choices.mechanism,
                               help_text=help_text.mechanism)
    rfam = StringProperty(max_length=100, help_text=help_text.rfam)
    description = StringProperty(help_text=help_text.generic_description)

    # relationships
    data_source = RelationshipTo('.source.Source', REL_TYPE, model=SourceRelationship)
    publication = RelationshipTo('.publication.Publication', REL_TYPE, model=BaseRelationship)
    regulator = RelationshipTo('.regulator.Regulator', REL_TYPE, model=BaseRelationship)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'name', 'mechanism', 'rfam', 'description',
                  'data_source', 'publication', 'regulator']
