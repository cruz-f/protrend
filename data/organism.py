from neomodel import StringProperty, IntegerProperty, RelationshipTo

from .base import BaseNode
from .relationships import REL_TYPE, SourceRelationship, BaseRelationship
from constants import help_text


class Organism(BaseNode):
    # properties
    name = StringProperty(required=True, max_length=200, help_text=help_text.organism_name)
    ncbi_taxonomy = IntegerProperty(help_text=help_text.ncbi_taxonomy)
    species = StringProperty(max_length=150, help_text=help_text.species)
    strain = StringProperty(max_length=150, help_text=help_text.strain)
    refseq_accession = StringProperty(max_length=50, help_text=help_text.refseq_accession)
    refseq_ftp = StringProperty(max_length=250, help_text=help_text.refseq_ftp)
    genbank_accession = StringProperty(max_length=50, help_text=help_text.genbank_accession)
    genbank_ftp = StringProperty(max_length=250, help_text=help_text.genbank_ftp)
    ncbi_assembly = IntegerProperty(help_text=help_text.ncbi_assembly)
    assembly_accession = StringProperty(max_length=50, help_text=help_text.assembly_accession)

    # relationships
    data_source = RelationshipTo('.source.Source', REL_TYPE, model=SourceRelationship)
    operon = RelationshipTo('.operon.Operon', REL_TYPE, model=BaseRelationship)
    regulator = RelationshipTo('.regulator.Regulator', REL_TYPE, model=BaseRelationship)
    gene = RelationshipTo('.gene.Gene', REL_TYPE, model=BaseRelationship)
    tfbs = RelationshipTo('.tfbs.TFBS', REL_TYPE, model=BaseRelationship)
    regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', REL_TYPE,
                                            model=BaseRelationship)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'name', 'ncbi_taxonomy', 'species', 'strain',
                  'refseq_accession', 'refseq_ftp', 'genbank_accession', 'genbank_ftp', 'ncbi_assembly',
                  'assembly_accession',
                  'data_source', 'operon', 'regulator', 'gene', 'tfbs', 'regulatory_interaction']