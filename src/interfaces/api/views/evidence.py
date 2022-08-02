from rest_framework import generics

import data
from interfaces import views, permissions
from interfaces.api import serializers


class EvidenceList(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Evidences available at ProTReND. Consult here the current list of all evidences in ProTReND.

    Evidences can be thought of as the experimental techniques and procedures that have lead to the discovery of the regulatory interactions listed in ProTReND.

    We are working on improving the descriptions of all evidences list in ProTReND.
    """
    serializer_class = serializers.EvidenceListSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.models.Evidence
    fields = ['protrend_id', 'name', 'description']


class EvidenceDetail(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Evidences available at ProTReND. Consult here all information available over this evidence.

    Evidences can be thought of as the experimental techniques and procedures that have lead to the discovery of the regulatory interactions listed in ProTReND.

    We are working on improving the descriptions of all evidences list in ProTReND.
    """
    serializer_class = serializers.EvidenceDetailSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.models.Evidence
    fields = ['protrend_id', 'name', 'description']
    targets = {'tfbs': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {}
