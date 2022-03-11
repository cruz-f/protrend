import rest_framework.permissions as drf_permissions
from drf_renderer_xlsx.renderers import XLSXRenderer
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_csv.renderers import CSVRenderer

import data
from interfaces import views, renderers
from interfaces.api import serializers


class TRNList(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Transcriptional Regulatory Networks (TRNs) available at ProTReND. Consult here the current list of all TRNs in ProTReND.

    TRNs encode instructions for the expression of target genes in response to regulatory proteins.
    TRNs can be thought of as computational modeling tools that allow to describe meaningful regulatory interactions between regulators and target genes.

    In ProTReND, a TRN is organism-specific and comprehends all these regulatory elements:
     - the regulator that mediates the control of gene expression
     - the target gene whose expression is being controlled by the regulatory element
     - the TFBS (might not be available for all interactions) where the regulator binds to activate/repress the target gene
     - the effector which can bind or not to a regulator altering the regulatory action of this element
     - the regulatory effect which consists of the outcome of the interaction between the regulator and the target gene, namely target gene activation, inactivation, dual or unknown behavior
    """
    serializer_class = serializers.TRNListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    model = data.Organism
    fields = ['protrend_id']


class TRN(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Transcriptional Regulatory Networks (TRNs) available at ProTReND. Consult here all information available over this TRN.

    TRNs encode instructions for the expression of target genes in response to regulatory proteins.
    TRNs can be thought of as computational modeling tools that allow to describe meaningful regulatory interactions between regulators and target genes.

    In ProTReND, a TRN is organism-specific and comprehends all these regulatory elements:
     - the regulator that mediates the control of gene expression
     - the target gene whose expression is being controlled by the regulatory element
     - the TFBS (might not be available for all interactions) where the regulator binds to activate/repress the target gene
     - the effector which can bind or not to a regulator altering the regulatory action of this element
     - the regulatory effect which consists of the outcome of the interaction between the regulator and the target gene, namely target gene activation, inactivation, dual or unknown behavior
    """
    serializer_class = serializers.TRNDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    model = data.Organism
    fields = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain']
    targets = {'regulatory_interaction': ['protrend_id', 'regulator', 'gene', 'tfbs', 'effector', 'regulatory_effect']}


class OrganismsBindingSites(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites datasets available at ProTReND. Consult here the current list of all Binding Sites datasets grouped by organism.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    The TFBS Dataset API allows one to retrieve all TFBSs associated with a single organism in several standard formats, such as FASTA.
    """
    serializer_class = serializers.OrganismBindingSitesListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    model = data.Organism
    fields = ['protrend_id']


class OrganismBindingSites(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites datasets available at ProTReND. Consult here the Binding Site dataset for the selected organism.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    The TFBS Dataset API allows one to retrieve all TFBSs associated with a single organism in several standard formats, such as FASTA
    """
    serializer_class = serializers.OrganismBindingSitesDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = (JSONRenderer, CSVRenderer, XLSXRenderer, renderers.FastaRenderer, BrowsableAPIRenderer)
    model = data.Organism
    fields = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain']
    targets = {'tfbs': ['protrend_id', 'sequence', 'strand', 'start', 'stop']}


class RegulatorsBindingSites(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites datasets available at ProTReND. Consult here the current list of all Binding Sites datasets grouped by regulator.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    The Regulator-TFBS Dataset API allows one to retrieve all TFBSs associated with a single regulator in several standard formats,
    such as FASTA.
    """
    serializer_class = serializers.RegulatorBindingSitesListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    model = data.Regulator
    fields = ['protrend_id']


class RegulatorBindingSites(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites datasets available at ProTReND. Consult here the Binding Sites dataset for the selected regulator.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    The Regulator-TFBS Dataset API allows one to retrieve all TFBSs associated with a single regulator in several standard formats,
    such as FASTA
    """
    serializer_class = serializers.RegulatorBindingSitesDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = (JSONRenderer, CSVRenderer, XLSXRenderer, renderers.FastaRenderer, BrowsableAPIRenderer)
    model = data.Regulator
    fields = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'mechanism']
    targets = {'tfbs': ['protrend_id', 'sequence', 'strand', 'start', 'stop']}
