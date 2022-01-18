from neomodel import StringProperty, IntegerProperty, DateTimeProperty, RelationshipTo
from neomodel import UniqueIdProperty

from .base import BaseNode
from .relationships import REL_TYPE


class Organism(BaseNode):
    uid = UniqueIdProperty()
    protrend_id = StringProperty(required=True)
    created = DateTimeProperty(default_now=True)
    updated = DateTimeProperty(default_now=True)

    # specific properties
    name = StringProperty(required=True)
    ncbi_taxonomy = IntegerProperty()
    species = StringProperty()
    strain = StringProperty()
    refseq_accession = StringProperty()
    refseq_ftp = StringProperty()
    genbank_accession = StringProperty()
    genbank_ftp = StringProperty()
    ncbi_assembly = IntegerProperty()
    assembly_accession = StringProperty()

    # relationships
    gene = RelationshipTo('Gene', REL_TYPE)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'name', 'ncbi_taxonomy', 'species', 'strain',
                  'refseq_accession', 'refseq_ftp', 'genbank_accession', 'genbank_ftp', 'ncbi_assembly',
                  'assembly_accession',
                  'gene']
