from django_neomodel import DjangoNode
from neomodel import UniqueIdProperty, StringProperty, DateTimeProperty, ArrayProperty, IntegerProperty

from .utils import help_text, choices


class BaseNode(DjangoNode):
    __abstract_node__ = True

    uid = UniqueIdProperty()
    protrend_id = StringProperty(required=True, unique_index=True, help_text=help_text.protrend_id)
    created = DateTimeProperty(default_now=True, help_text=help_text.created)
    updated = DateTimeProperty(default_now=True, help_text=help_text.updated)

    class Meta:
        app_label = 'data'
        order_by = ['protrend_id']


class RequiredNameMixIn:
    # properties
    name = StringProperty(required=True, max_length=250, help_text=help_text.required_name)


class SequenceMixIn:
    sequence = StringProperty(help_text=help_text.sequence)


class PositionMixIn:
    strand = StringProperty(choices=choices.strand, help_text=help_text.strand)
    start = IntegerProperty(help_text=help_text.start)
    stop = IntegerProperty(help_text=help_text.stop)


class GeneMixIn:
    # properties
    locus_tag = StringProperty(required=True, max_length=50, help_text=help_text.locus_tag)
    uniprot_accession = StringProperty(max_length=50, help_text=help_text.uniprot_accession)
    name = StringProperty(max_length=50, help_text=help_text.gene_name)
    synonyms = ArrayProperty(StringProperty(), help_text=help_text.synonyms)
    function = StringProperty(help_text=help_text.function)
    description = StringProperty(help_text=help_text.description)
    ncbi_gene = IntegerProperty(max_length=50, help_text=help_text.ncbi_gene)
    ncbi_protein = IntegerProperty(max_length=50, help_text=help_text.ncbi_protein)
    genbank_accession = StringProperty(max_length=50, help_text=help_text.genbank_accession)
    refseq_accession = StringProperty(max_length=50, help_text=help_text.refseq_accession)