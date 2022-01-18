from neomodel import RelationshipTo, One

from .base import BaseNode, GeneMixIn, SequenceMixIn, PositionMixIn
from .relationships import REL_TYPE, SourceRelationship


class Gene(BaseNode, GeneMixIn, SequenceMixIn, PositionMixIn):
    # base
    entity = 'GEN'

    # properties inherited from GeneMixIn, SequenceMixIn, PositionMixIn

    # relationships
    data_source = RelationshipTo('.source.Source', REL_TYPE, model=SourceRelationship)
    evidence = RelationshipTo('.evidence.Evidence', REL_TYPE)
    publication = RelationshipTo('.publication.Publication', REL_TYPE)
    pathway = RelationshipTo('.pathway.Pathway', REL_TYPE)
    operon = RelationshipTo('.operon.Operon', REL_TYPE)
    organism = RelationshipTo('.organism.Organism', REL_TYPE, cardinality=One)
    regulator = RelationshipTo('.regulator.Regulator', REL_TYPE)
    tfbs = RelationshipTo('.tfbs.TFBS', REL_TYPE)
    regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', REL_TYPE)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'locus_tag', 'uniprot_accession', 'name', 'synonyms',
                  'function', 'description', 'ncbi_gene', 'ncbi_protein', 'genbank_accession', 'refseq_accession',
                  'sequence', 'strand', 'start', 'stop',
                  'data_source', 'evidence', 'publication', 'pathway', 'operon', 'organism', 'regulator',
                  'tfbs', 'regulatory_interaction']
