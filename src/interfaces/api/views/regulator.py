from rest_framework import generics

import data
from interfaces import views, permissions
from interfaces.api import serializers


class RegulatorList(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulators available at ProTReND. Consult here the current list of all regulators in ProTReND.

    A regulator consists of a Transcription Factor, Sigma Factor, small RNA (sRNA), Transcription attenuator, or Transcription Terminator. In detail, a regulator can be considered a regulatory protein or RNA regulatory element that mediates the control of gene expression.
    Target genes can be activated or repressed by the binding (or not) of these regulatory elements.

    Regulators are composed by a sequence of nucleotides in DNA that encodes a given RNA or protein. Several details are available for each regulator including for instance locus tag, name, synonyms, and function. The corresponding protein sequence and genomic coordinates can also be consulted in the REST API.
    Most regulators are referenced to widely known databases, such as UniProt, NCBI protein and NCBI gene, by the corresponding identifiers.
    Finally, the mechanism of control of the gene expression is available for each regulator.
    """
    serializer_class = serializers.RegulatorListSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.models.Regulator
    fields = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms', 'mechanism']


class RegulatorDetail(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulators available at ProTReND. Consult here all information available over this regulator.

    A regulator consists of a Transcription Factor, Sigma Factor, small RNA (sRNA), Transcription attenuator, or Transcription Terminator. In detail, a regulator can be considered a regulatory protein or RNA regulatory element that mediates the control of gene expression.
    Target genes can be activated or repressed by the binding (or not) of these regulatory elements.

    Regulators are composed by a sequence of nucleotides in DNA that encodes a given RNA or protein. Several details are available for each regulator including for instance locus tag, name, synonyms, and function. The corresponding protein sequence and genomic coordinates can also be consulted in the REST API.
    Most regulators are referenced to widely known databases, such as UniProt, NCBI protein and NCBI gene, by the corresponding identifiers.
    Finally, the mechanism of control of the gene expression is available for each regulator.
    """
    serializer_class = serializers.RegulatorDetailSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.models.Regulator
    fields = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms', 'mechanism',
              'function', 'description', 'ncbi_gene',
              'ncbi_protein', 'genbank_accession', 'refseq_accession', 'sequence', 'strand', 'start', 'stop']
    targets = {'data_source': ['name', 'url'],
               'organism': ['protrend_id'],
               'effector': ['protrend_id'],
               'gene': ['protrend_id'],
               'tfbs': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {'data_source': ['url']}
