from neomodel import StringProperty, IntegerProperty, RelationshipTo

from .base import BaseNode
from .relationships import BASE_REL_TYPE, BaseRelationship
from constants import help_text


class Publication(BaseNode):
    # properties
    pmid = IntegerProperty(required=True, unique_index=True, help_text=help_text.pmid)
    pmid_factor = IntegerProperty(required=True, unique_index=True, help_text=help_text.pmid)
    doi = StringProperty(max_length=250, help_text=help_text.doi)
    title = StringProperty(max_length=500, help_text=help_text.title)
    author = StringProperty(max_length=250, help_text=help_text.author)
    year = IntegerProperty(help_text=help_text.year)

    # relationships
    regulatory_family = RelationshipTo('.regulatory_family.RegulatoryFamily', BASE_REL_TYPE, model=BaseRelationship)
    regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    operon = RelationshipTo('.operon.Operon', BASE_REL_TYPE, model=BaseRelationship)
    gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)
    tfbs = RelationshipTo('.tfbs.TFBS', BASE_REL_TYPE, model=BaseRelationship)
    regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', BASE_REL_TYPE,
                                            model=BaseRelationship)
