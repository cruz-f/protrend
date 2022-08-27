from rest_framework import generics
from drf_renderer_xlsx.renderers import XLSXRenderer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_csv.renderers import CSVRenderer

import data
from interfaces import views, permissions
from interfaces.api import serializers
from interfaces.renderers import NucleotideFastaRenderer, AminoAcidFastaRenderer, \
    NucleotideGenBankRenderer, AminoAcidGenBankRenderer


class GeneList(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Genes available at ProTReND. Consult here the current list of all genes in ProTReND.

    Genes are composed by a sequence of nucleotides in DNA that encodes a given RNA or protein. In this case, most genes listed in ProTReND are implicity target genes for a set of regulators.
    In detail, ProTReND genes are involved in regulatory interactions. The expression of these genes can be mediated by one or more regulators available at ProTReND.

    Several details are available for each gene including for instance locus tag, name, synonyms, and function. The corresponding protein sequence and genomic coordinates can also be consulted in the REST API.
    Most genes are referenced to widely known databases, such as UniProt, NCBI protein and NCBI gene, by the corresponding identifiers
    """
    serializer_class = serializers.GeneListSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.models.Gene
    fields = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms']


class GeneDetail(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Genes available at ProTReND. Consult here all information available over this gene.

    Genes are composed by a sequence of nucleotides in DNA that encodes a given RNA or protein. In this case, most genes listed in ProTReND are implicity target genes for a set of regulators.
    In detail, ProTReND genes are involved in regulatory interactions. The expression of these genes can be mediated by one or more regulators available at ProTReND.

    Several details are available for each gene including for instance locus tag, name, synonyms, and function. The corresponding protein sequence and genomic coordinates can also be consulted in the REST API.
    Most genes are referenced to widely known databases, such as UniProt, NCBI protein and NCBI gene, by the corresponding identifiers
    """
    serializer_class = serializers.GeneDetailSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    renderer_classes = (JSONRenderer, CSVRenderer, XLSXRenderer,
                        NucleotideFastaRenderer, AminoAcidFastaRenderer,
                        NucleotideGenBankRenderer, AminoAcidGenBankRenderer,
                        BrowsableAPIRenderer)
    model = data.models.Gene
    fields = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms',
              'function', 'description', 'ncbi_gene', 'ncbi_protein',
              'genbank_accession', 'refseq_accession', 'gene_sequence', 'protein_sequence', 'strand', 'start', 'stop']
    targets = {'data_source': ['name', 'url'],
               'organism': ['protrend_id'],
               'operon': ['protrend_id'],
               'regulator': ['protrend_id'],
               'tfbs': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {'data_source': ['url']}
