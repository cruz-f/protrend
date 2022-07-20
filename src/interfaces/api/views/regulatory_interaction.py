from typing import Union

from rest_framework import generics

import data
from interfaces import views, permissions
from interfaces.api import serializers
from utils import get_header


class InteractionsList(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulatory Interactions available at ProTReND. Consult here the current list of all interactions in ProTReND.

    A regulatory interaction consists of the biological phenomena that involves the control of gene expression by a given regulator. In detail, a regulator activates or represses the expression of its target genes.
    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression. In addition, the regulatory actions promoted by a given regulator can also be influenced by biochemical molecules or metabolites called regulatory effectors.

    In ProTReND, a regulatory interaction comprehends all these regulatory elements:
     - the organism where the regulatory interaction takes place
     - the regulator that mediates the control of gene expression
     - the target gene whose expression is being controlled by the regulatory element
     - the TFBS (might not be available for all interactions) where the regulator binds to activate/repress the target gene
     - the effector which can bind or not to a regulator altering the regulatory action of this element
     - the regulatory effect which consists of the outcome of the interaction between the regulator and the target gene, namely target gene activation, inactivation, dual or unknown behavior
    """
    serializer_class = serializers.RegulatoryInteractionListSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.models.RegulatoryInteraction
    fields = ['protrend_id', 'organism', 'regulator', 'gene', 'tfbs', 'effector', 'regulatory_effect']


class InteractionDetail(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulatory Interactions available at ProTReND. Consult here all information available over this interaction.

    A regulatory interaction consists of the biological phenomena that involves the control of gene expression by a given regulator. In detail, a regulator activates or represses the expression of its target genes.
    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression. In addition, the regulatory actions promoted by a given regulator can also be influenced by biochemical molecules or metabolites called regulatory effectors.

    In ProTReND, a regulatory interaction comprehends all these regulatory elements:
     - the organism where the regulatory interaction takes place
     - the regulator that mediates the control of gene expression
     - the target gene whose expression is being controlled by the regulatory element
     - the TFBS (might not be available for all interactions) where the regulator binds to activate/repress the target gene
     - the effector which can bind or not to a regulator altering the regulatory action of this element
     - the regulatory effect which consists of the outcome of the interaction between the regulator and the target gene, namely target gene activation, inactivation, dual or unknown behavior
    """
    serializer_class = serializers.RegulatoryInteractionDetailSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.models.RegulatoryInteraction
    fields = ['protrend_id', 'regulatory_effect']
    targets = {'data_source': ['name', 'url'],
               'evidence': ['protrend_id'],
               'publication': ['protrend_id'],
               'data_organism': ['protrend_id', 'name', 'ncbi_taxonomy'],
               'data_effector': ['protrend_id', 'name'],
               'data_regulator': ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'mechanism'],
               'data_gene': ['protrend_id', 'locus_tag', 'uniprot_accession', 'name'],
               'data_tfbs': ['protrend_id', 'sequence', 'strand', 'start', 'stop', ]}
    relationships = {'data_source': ['url']}

    def get_renderer_context(self: Union['views.APIListView', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        nested_fields = ('organism', 'regulator', 'gene', 'tfbs', 'effector')
        header, _ = get_header(serializer_cls=serializer_cls, nested_fields=nested_fields)

        context['header'] = header
        return context
