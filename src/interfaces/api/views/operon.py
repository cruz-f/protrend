from typing import Union

from rest_framework import generics

import data
from interfaces import views, permissions
from interfaces.api import serializers
from utils import get_header


class OperonList(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Operons available at ProTReND. Consult here the current list of all operons in ProTReND.

    An operon is based on a set of genes which are usually transcribed together as a single unit called a polycistronic unit.

    Several details are available for each operon including the set of genes that compose the operon in ProTReND.
    The corresponding genomic coordinates can also be consulted in the REST API.

    All operons have been retrieved from OperonDB (https://operondb.jp/). Hence, one can consult the OperonDB identifier for each operon listed in ProTReND.
    We advise you to consult OperonDB for more details.
    """
    serializer_class = serializers.OperonListSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.Operon
    fields = ['protrend_id', 'operon_db_id', 'name', 'function', 'genes']


class OperonDetail(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Operons available at ProTReND. Consult here all information available over this operon and its genes.

    An operon is based on a set of genes which are usually transcribed together as a single unit called a polycistronic unit.

    Several details are available for each operon including the set of genes that compose the operon in ProTReND.
    The corresponding genomic coordinates can also be consulted in the REST API.

    All operons have been retrieved from OperonDB (https://operondb.jp/). Hence, one can consult the OperonDB identifier for each operon listed in ProTReND.
    We advise you to consult OperonDB for more details.
    """
    serializer_class = serializers.OperonDetailSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.Operon
    fields = ['protrend_id', 'operon_db_id', 'name', 'function', 'genes', 'strand', 'start', 'stop']
    targets = {'data_source': ['name', 'url'],
               'organism': ['protrend_id'],
               'gene': ['protrend_id', 'locus_tag', 'uniprot_accession', 'name']}
    relationships = {'data_source': ['url']}

    def get_renderer_context(self: Union['views.APIListView', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        nested_fields = ('genes',)
        header, _ = get_header(serializer_cls=serializer_cls, nested_fields=nested_fields)

        context['header'] = header
        return context
