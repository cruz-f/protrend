from neomodel import StringProperty, RelationshipTo

from .base import BaseNode, RequiredNameMixIn
from .relationships import REL_TYPE, SourceRelationship
from .utils import help_text, choices, default


class RegulatoryFamily(BaseNode, RequiredNameMixIn):
    entity = 'RFAM'

    # properties
    mechanism = StringProperty(required=True, choices=choices.mechanism,
                               default=default.mechanism, max_length=50,
                               help_text=help_text.mechanism)
    rfam = StringProperty(max_length=100, help_text=help_text.rfam)
    description = StringProperty(help_text=help_text.generic_description)

    # relationships
    data_source = RelationshipTo('.source.Source', REL_TYPE, model=SourceRelationship)
    publication = RelationshipTo('.publication.Publication', REL_TYPE)
    regulator = RelationshipTo('.regulator.Regulator', REL_TYPE)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'name', 'mechanism', 'rfam', 'description',
                  'data_source', 'publication', 'regulator']
