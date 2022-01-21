from neomodel import StringProperty, IntegerProperty, RelationshipTo

from .base import BaseNode
from .relationships import REL_TYPE, BaseRelationship
from constants import help_text


class Publication(BaseNode):
    # properties
    pmid = IntegerProperty(required=True, unique_index=True, help_text=help_text.pmid)
    doi = StringProperty(max_length=250, help_text=help_text.doi)
    title = StringProperty(max_length=500, help_text=help_text.title)
    author = StringProperty(max_length=250, help_text=help_text.author)
    year = IntegerProperty(help_text=help_text.year)

    # relationships
    regulatory_family = RelationshipTo('.regulatory_family.RegulatoryFamily', REL_TYPE, model=BaseRelationship)
    regulator = RelationshipTo('.regulator.Regulator', REL_TYPE, model=BaseRelationship)
    operon = RelationshipTo('.operon.Operon', REL_TYPE, model=BaseRelationship)
    gene = RelationshipTo('.gene.Gene', REL_TYPE, model=BaseRelationship)
    tfbs = RelationshipTo('.tfbs.TFBS', REL_TYPE, model=BaseRelationship)
    regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', REL_TYPE,
                                            model=BaseRelationship)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'pmid', 'doi', 'title', 'author', 'year',
                  'regulatory_family', 'regulator', 'operon', 'gene', 'tfbs', 'regulatory_interaction']
