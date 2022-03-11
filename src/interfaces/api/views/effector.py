import rest_framework.permissions as drf_permissions
from rest_framework import generics

import data
from interfaces import views, permissions
from interfaces.api import serializers


class EffectorList(views.APIListView, views.APICreateView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Effectors available at ProTReND. Consult here the current list of all effectors in ProTReND.

    Effectors can be defined as the biochemical elements that either bind to a given regulator or influence the regulator activity. These biological phenomena can alter the regulator afinity to Transcription Factor Binding Sites (TFBS) and thus changing the regulatory interaction between the regulator and target genes.
    Most effectors can bind to a given regulator which ends up blocking transcription sites.

    Note that, we only provide the effector name and potential associated KEGG compounds. We are working on improving the information provided for each effector.
    """
    serializer_class = serializers.EffectorListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Effector
    fields = ['protrend_id', 'name', 'kegg_compounds']


class EffectorDetail(views.APIRetrieveView, views.APIUpdateDestroyView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Effectors available at ProTReND. Consult here all information available over this effector.

    Effectors can be defined as the biochemical elements that either bind to a given regulator or influence the regulator activity. These biological phenomena can alter the regulator afinity to Transcription Factor Binding Sites (TFBS) and thus changing the regulatory interaction between the regulator and target genes.
    Most effectors can bind to a given regulator which ends up blocking transcription sites.

    Note that, we only provide the effector name and potential associated KEGG compounds. We are working on improving the information provided for each effector.
    """
    serializer_class = serializers.EffectorDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Effector
    fields = ['protrend_id', 'name', 'kegg_compounds']
    targets = {'data_source': ['name', 'url'],
               'regulator': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {'data_source': ['url']}