from neomodel import RelationshipTo, ZeroOrOne, StringProperty, ArrayProperty, IntegerProperty

from constants import help_text, choices
from .base import BaseNode
from .relationships import BASE_REL_TYPE, SourceRelationship, BaseRelationship, SOURCE_REL_TYPE


class Gene(BaseNode):
    # properties
    locus_tag = StringProperty(required=True, unique_index=True, max_length=100, help_text=help_text.locus_tag)
    locus_tag_factor = StringProperty(required=True, unique_index=True, max_length=100,
                                      help_text=help_text.locus_tag)
    uniprot_accession = StringProperty(unique_index=True, max_length=50, help_text=help_text.uniprot_accession)
    uniprot_accession_factor = StringProperty(unique_index=True, max_length=50, help_text=help_text.uniprot_accession)
    name = StringProperty(max_length=50, help_text=help_text.gene_name)
    synonyms = ArrayProperty(StringProperty(), help_text=help_text.synonyms)
    function = StringProperty(help_text=help_text.function)
    description = StringProperty(help_text=help_text.description)
    ncbi_gene = IntegerProperty(max_length=50, help_text=help_text.ncbi_gene)
    ncbi_protein = IntegerProperty(max_length=50, help_text=help_text.ncbi_protein)
    genbank_accession = StringProperty(max_length=50, help_text=help_text.genbank_accession)
    refseq_accession = StringProperty(max_length=50, help_text=help_text.refseq_accession)
    protein_sequence = StringProperty(help_text=help_text.protein_sequence)
    gene_sequence = StringProperty(help_text=help_text.gene_sequence)
    strand = StringProperty(choices=choices.strand, help_text=help_text.strand)
    start = IntegerProperty(help_text=help_text.start)
    stop = IntegerProperty(help_text=help_text.stop)

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
