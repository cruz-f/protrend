from neomodel import StringProperty, RelationshipTo, ZeroOrOne

from constants import choices, help_text
from .base import BaseNode, GeneMixIn, SequenceMixIn, PositionMixIn
from .relationships import REL_TYPE, SourceRelationship, BaseRelationship


class Regulator(BaseNode, GeneMixIn, SequenceMixIn, PositionMixIn):
    # properties
    mechanism = StringProperty(required=True, choices=choices.mechanism,
                               help_text=help_text.mechanism)

    # properties inherited from GeneMixIn, SequenceMixIn, PositionMixIn

    # relationships
    data_source = RelationshipTo('.source.Source', REL_TYPE, model=SourceRelationship)
    evidence = RelationshipTo('.evidence.Evidence', REL_TYPE, model=BaseRelationship)
    publication = RelationshipTo('.publication.Publication', REL_TYPE, model=BaseRelationship)
    pathway = RelationshipTo('.pathway.Pathway', REL_TYPE, model=BaseRelationship)
    effector = RelationshipTo('.effector.Effector', REL_TYPE, model=BaseRelationship)
    regulatory_family = RelationshipTo('.regulatory_family.RegulatoryFamily', REL_TYPE, cardinality=ZeroOrOne,
                                       model=BaseRelationship)
    organism = RelationshipTo('.organism.Organism', REL_TYPE, cardinality=ZeroOrOne, model=BaseRelationship)
    gene = RelationshipTo('.gene.Gene', REL_TYPE, model=BaseRelationship)
    tfbs = RelationshipTo('.tfbs.TFBS', REL_TYPE, model=BaseRelationship)
    regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', REL_TYPE,
                                            model=BaseRelationship)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'locus_tag', 'uniprot_accession', 'name', 'synonyms',
                  'function', 'description', 'ncbi_gene', 'ncbi_protein', 'genbank_accession', 'refseq_accession',
                  'sequence', 'strand', 'start', 'stop', 'mechanism',
                  'data_source', 'evidence', 'publication', 'pathway', 'effector', 'regulatory_family',
                  'organism', 'gene', 'tfbs', 'regulatory_interaction']
