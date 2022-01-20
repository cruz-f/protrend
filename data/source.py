from neomodel import StringProperty, RelationshipTo, ArrayProperty

from .base import BaseNode, RequiredNameMixIn
from .relationships import REL_TYPE, SourceRelationship
from constants import help_text, choices


class Source(BaseNode, RequiredNameMixIn):
    # properties
    type = StringProperty(required=True, choices=choices.data_source_type,
                          help_text=help_text.data_source_type)
    url = StringProperty(max_length=300, help_text=help_text.url)
    doi = StringProperty(max_length=250, help_text=help_text.doi)
    authors = ArrayProperty(StringProperty(), help_text=help_text.source_author)
    description = StringProperty(help_text=help_text.generic_description)

    # relationships
    organism = RelationshipTo('.organism.Organism', REL_TYPE, model=SourceRelationship)
    pathway = RelationshipTo('.pathway.Pathway', REL_TYPE, model=SourceRelationship)
    regulatory_family = RelationshipTo('.regulatory_family.RegulatoryFamily', REL_TYPE, model=SourceRelationship)
    regulator = RelationshipTo('.regulator.Regulator', REL_TYPE, model=SourceRelationship)
    operon = RelationshipTo('.operon.Operon', REL_TYPE, model=SourceRelationship)
    gene = RelationshipTo('.gene.Gene', REL_TYPE, model=SourceRelationship)
    tfbs = RelationshipTo('.tfbs.TFBS', REL_TYPE, model=SourceRelationship)
    effector = RelationshipTo('.effector.Effector', REL_TYPE, model=SourceRelationship)
    regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', REL_TYPE,
                                            model=SourceRelationship)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'name', 'type', 'url', 'doi', 'authors', 'description',
                  'organism', 'pathway', 'regulatory_family', 'regulator', 'operon', 'gene',
                  'tfbs', 'effector', 'regulatory_interaction']