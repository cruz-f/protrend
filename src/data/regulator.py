from neomodel import StringProperty, RelationshipTo, ZeroOrOne

from constants import choices, help_text
from .base import BaseNode, GeneMixIn, SequenceMixIn, PositionMixIn
from .relationships import BASE_REL_TYPE, SourceRelationship, BaseRelationship, SOURCE_REL_TYPE


class Regulator(BaseNode, GeneMixIn, SequenceMixIn, PositionMixIn):
    # properties
    mechanism = StringProperty(required=True, choices=choices.mechanism,
                               help_text=help_text.mechanism)

    # properties inherited from GeneMixIn, SequenceMixIn, PositionMixIn

    # relationships
    data_source = RelationshipTo('.source.Source', SOURCE_REL_TYPE, model=SourceRelationship)
    evidence = RelationshipTo('.evidence.Evidence', BASE_REL_TYPE, model=BaseRelationship)
    publication = RelationshipTo('.publication.Publication', BASE_REL_TYPE, model=BaseRelationship)
    pathway = RelationshipTo('.pathway.Pathway', BASE_REL_TYPE, model=BaseRelationship)
    effector = RelationshipTo('.effector.Effector', BASE_REL_TYPE, model=BaseRelationship)
    regulatory_family = RelationshipTo('.regulatory_family.RegulatoryFamily', BASE_REL_TYPE, cardinality=ZeroOrOne,
                                       model=BaseRelationship)
    organism = RelationshipTo('.organism.Organism', BASE_REL_TYPE, cardinality=ZeroOrOne, model=BaseRelationship)
    gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)
    tfbs = RelationshipTo('.tfbs.TFBS', BASE_REL_TYPE, model=BaseRelationship)
    regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', BASE_REL_TYPE,
                                            model=BaseRelationship)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'locus_tag', 'uniprot_accession', 'name', 'synonyms',
                  'function', 'description', 'ncbi_gene', 'ncbi_protein', 'genbank_accession', 'refseq_accession',
                  'sequence', 'strand', 'start', 'stop', 'mechanism',
                  'data_source', 'evidence', 'publication', 'pathway', 'effector', 'regulatory_family',
                  'organism', 'gene', 'tfbs', 'regulatory_interaction']
