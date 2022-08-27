import rest_framework.permissions as drf_permissions
from drf_renderer_xlsx.renderers import XLSXRenderer
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_csv.renderers import CSVRenderer

import data
from interfaces import views
from interfaces.api import serializers
from interfaces.renderers import JASPARRenderer, TRANSFACRenderer


class MotifList(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Motifs available at ProTReND. Consult here the current list of all Motifs grouped by regulator.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    All binding site sequences associated with a given regulator have been aligned using the LASAGNA algorithm.

    The Motif API allows one to retrieve all TFBSs associated with a single regulator in several standard formats, such as FASTA.
    """
    serializer_class = serializers.MotifListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    model = data.models.Motif
    fields = ['protrend_id', 'regulator', 'tfbs', 'sequences', 'consensus_sequence']


class MotifDetail(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Motifs available at ProTReND. Consult here the Motif for the selected regulator.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    All binding site sequences associated with a given regulator have been aligned using the LASAGNA algorithm.

    The Motif API allows one to retrieve all TFBSs associated with a single regulator in several standard formats, such as FASTA
    """
    serializer_class = serializers.MotifDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = (JSONRenderer, CSVRenderer, XLSXRenderer, JASPARRenderer, TRANSFACRenderer, BrowsableAPIRenderer)
    model = data.models.Motif
    fields = ['protrend_id', 'sequences', 'consensus_sequence']
    targets = {'organism': ['protrend_id', 'name', 'ncbi_taxonomy'],
               'data_regulator': ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'mechanism'],
               'data_tfbs': ['protrend_id']}
    relationships = {'data_tfbs': ['sequence', 'strand', 'start', 'stop']}
