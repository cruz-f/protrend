from neomodel import StringProperty, IntegerProperty, DateTimeProperty, ArrayProperty, RelationshipTo
from neomodel import UniqueIdProperty

from .base import BaseNode
from .relationships import REL_TYPE


class Gene(BaseNode):

    uid = UniqueIdProperty()
    protrend_id = StringProperty(required=True)
    created = DateTimeProperty(default_now=True)
    updated = DateTimeProperty(default_now=True)

    # specific properties
    locus_tag = StringProperty(required=True)
    uniprot_accession = StringProperty()
    name = StringProperty()
    synonyms = ArrayProperty(StringProperty())
    function = StringProperty()
    description = StringProperty()
    ncbi_gene = IntegerProperty()
    ncbi_protein = IntegerProperty()
    genbank_accession = StringProperty()
    refseq_accession = StringProperty()
    sequence = StringProperty()
    strand = StringProperty()
    start = IntegerProperty()
    stop = IntegerProperty()

    # relationships
    organism = RelationshipTo('.organism.Organism', REL_TYPE)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'locus_tag', 'uniprot_accession', 'name', 'synonyms',
                  'function', 'description', 'ncbi_gene', 'ncbi_protein', 'genbank_accession', 'refseq_accession',
                  'sequence', 'strand', 'start', 'stop',
                  'organism']
