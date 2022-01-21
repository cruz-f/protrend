from neomodel import StringProperty, RelationshipTo, IntegerProperty, One

from .base import BaseNode, SequenceMixIn, PositionMixIn
from .relationships import BASE_REL_TYPE, SourceRelationship, BaseRelationship, SOURCE_REL_TYPE
from constants import help_text


class TFBS(BaseNode, SequenceMixIn, PositionMixIn):
    # properties
    site_hash = StringProperty(required=True, unique_index=True, max_length=600)
    organism = StringProperty(required=True, max_length=100, help_text=help_text.organism_id)
    length = IntegerProperty(required=True, help_text=help_text.length)

    # relationships
    data_source = RelationshipTo('.source.Source', SOURCE_REL_TYPE, model=SourceRelationship)
    evidence = RelationshipTo('.evidence.Evidence', BASE_REL_TYPE, model=BaseRelationship)
    publication = RelationshipTo('.publication.Publication', BASE_REL_TYPE, model=BaseRelationship)
    data_organism = RelationshipTo('.organism.Organism', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)
    regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', BASE_REL_TYPE,
                                            model=BaseRelationship)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'organism', 'sequence', 'strand', 'start', 'stop', 'length',
                  'data_source', 'evidence', 'publication', 'organism', 'regulator', 'gene', 'regulatory_interaction']
