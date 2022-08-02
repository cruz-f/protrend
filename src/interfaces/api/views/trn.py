import rest_framework.permissions as drf_permissions
from rest_framework import generics

import data
from interfaces import views
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
    model = data.models.Organism
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
    model = data.models.Organism
    fields = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain']
    targets = {'regulatory_interaction': ['protrend_id', 'regulator', 'gene', 'tfbs', 'effector', 'regulatory_effect']}
