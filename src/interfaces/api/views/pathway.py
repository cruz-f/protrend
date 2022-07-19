from rest_framework import generics

import data
from interfaces import views, permissions
from interfaces.api import serializers


class PathwayList(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Pathways available at ProTReND. Consult here the current list of all pathways in ProTReND.

    A metabolic pathway consists of a set of biochemical reactions occurring within a cellular organism.
    At ProTReND, we provide the name of the metabolic pathways associated with regulators and genes.
    In addition, potential KEGG Pathway identifiers are also provided for each pathway listed here.

    Note that, we only provide the pathway name and potential associated KEGG Pathways. We are working on improving the information provided for each pathway.
    """
    serializer_class = serializers.PathwayListSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.Pathway
    fields = ['protrend_id', 'name', 'kegg_pathways']


class PathwayDetail(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Pathways available at ProTReND. Consult here all information available over this pathway.

    A metabolic pathway consists of a set of biochemical reactions occurring within a cellular organism.
    At ProTReND, we provide the name of the metabolic pathways associated with regulators and genes.
    In addition, potential KEGG Pathway identifiers are also provided for each pathway listed here.

    Note that, we only provide the pathway name and potential associated KEGG Pathways. We are working on improving the information provided for each pathway.
    """
    serializer_class = serializers.PathwayDetailSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.Pathway
    fields = ['protrend_id', 'name', 'kegg_pathways']
    targets = {'data_source': ['name', 'url'],
               'regulator': ['protrend_id'],
               'gene': ['protrend_id']}
    relationships = {'data_source': ['url']}
