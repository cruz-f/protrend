import rest_framework.permissions as drf_permissions
from rest_framework import generics

import data
from interfaces import views, permissions
from interfaces.api import serializers


class RegulatoryFamilyList(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulatory Families available at ProTReND. Consult here the current list of all rfams in ProTReND.

    A regulatory family comprehends a set of regulators that either share homology among each other, or similar regulatory mechanisms, or common regulatory structures.
    Most regulators are linked to a common regulatory family according to the collected data sources.

    Note that, we only provide the rfam name and sometimes the rfam identifiers. We are working on improving the information provided for each regulatory family.
    """
    serializer_class = serializers.RegulatoryFamilyListSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.models.RegulatoryFamily
    fields = ['protrend_id', 'name', 'mechanism']


class RegulatoryFamilyDetail(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulatory Families available at ProTReND. Consult here all information available over this rfam.

    A regulatory family comprehends a set of regulators that either share homology among each other, or similar regulatory mechanisms, or common regulatory structures.
    Most regulators are linked to a common regulatory family according to the collected data sources.

    Note that, we only provide the rfam name and sometimes the rfam identifiers. We are working on improving the information provided for each regulatory family.
    """
    serializer_class = serializers.RegulatoryFamilyDetailSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.models.RegulatoryFamily
    fields = ['protrend_id', 'name', 'mechanism', 'rfam', 'description']
    targets = {'data_source': ['name', 'url'],
               'regulator': ['protrend_id']}
    relationships = {'data_source': ['url']}
