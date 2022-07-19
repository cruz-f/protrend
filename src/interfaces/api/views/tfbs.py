from typing import Union

from rest_framework import generics

import data
from interfaces import views, permissions
from interfaces.api import serializers
from utils import get_header


class BindingSitesList(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites available at ProTReND. Consult here the current list of all binding sites in ProTReND.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    Note that, a binding site might not be regulator-specific. Although these events are extremely rare, more than one regulator can bind to the same cis-element.
    """
    serializer_class = serializers.TFBSListSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.TFBS
    fields = ['protrend_id', 'organism', 'sequence', 'strand', 'start', 'stop', 'length']


class BindingSiteDetail(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites available at ProTReND. Consult here all information available over this binding site.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    Note that, a binding site might not be regulator-specific. Although these events are extremely rare, more than one regulator can bind to the same cis-element.
    """
    serializer_class = serializers.TFBSDetailSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.TFBS
    fields = ['protrend_id', 'organism', 'sequence', 'strand', 'start', 'stop', 'length']
    targets = {'data_source': ['name', 'url'],
               'evidence': ['protrend_id'],
               'publication': ['protrend_id'],
               'data_organism': ['protrend_id', 'name', 'ncbi_taxonomy'],
               'regulator': ['protrend_id'],
               'gene': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {'data_source': ['url']}

    def get_renderer_context(self: Union['views.APIListView', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        nested_fields = ('organism',)
        header, _ = get_header(serializer_cls=serializer_cls, nested_fields=nested_fields)

        context['header'] = header
        return context
