from neomodel import RelationshipTo, ZeroOrOne

from .base import BaseNode, GeneMixIn, SequenceMixIn, PositionMixIn
from .relationships import BASE_REL_TYPE, SourceRelationship, BaseRelationship, SOURCE_REL_TYPE


class Gene(BaseNode, GeneMixIn, SequenceMixIn, PositionMixIn):
    # properties inherited from GeneMixIn, SequenceMixIn, PositionMixIn

    # relationships
    data_source = RelationshipTo('.source.Source', SOURCE_REL_TYPE, model=SourceRelationship)
    evidence = RelationshipTo('.evidence.Evidence', BASE_REL_TYPE, model=BaseRelationship)
    publication = RelationshipTo('.publication.Publication', BASE_REL_TYPE, model=BaseRelationship)
    pathway = RelationshipTo('.pathway.Pathway', BASE_REL_TYPE, model=BaseRelationship)
    operon = RelationshipTo('.operon.Operon', BASE_REL_TYPE, model=BaseRelationship)
    organism = RelationshipTo('.organism.Organism', BASE_REL_TYPE, cardinality=ZeroOrOne, model=BaseRelationship)
    regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    tfbs = RelationshipTo('.tfbs.TFBS', BASE_REL_TYPE, model=BaseRelationship)
    regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', BASE_REL_TYPE,
                                            model=BaseRelationship)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'locus_tag', 'uniprot_accession', 'name', 'synonyms',
                  'function', 'description', 'ncbi_gene', 'ncbi_protein', 'genbank_accession', 'refseq_accession',
                  'sequence', 'strand', 'start', 'stop',
                  'data_source', 'evidence', 'publication', 'pathway', 'operon', 'organism', 'regulator',
                  'tfbs', 'regulatory_interaction']
