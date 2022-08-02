from rest_framework import generics

import data
from interfaces import views, permissions
from interfaces.api import serializers


class PublicationList(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Publications available at ProTReND. Consult here the current list of all publications in ProTReND.

    A publication consists of a manuscript published in a scientific jornal, a chapter of a scientific book, among others. Most ublications are associated to regulators, genes, and regulatory interactions, and thus supporting regulatory phenomena with exeperimental evidences.

    Note that, we only provide the main details of each publication. The publication can then be consulted using the DOI or PMID.
    """
    serializer_class = serializers.PublicationListSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.models.Publication
    fields = ['protrend_id', 'pmid', 'doi', 'title', 'author', 'year']


class PublicationDetail(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Publications available at ProTReND. Consult here all information available over this publication.

    A publication consists of a manuscript published in a scientific jornal, a chapter of a scientific book, among others. Most ublications are associated to regulators, genes, and regulatory interactions, and thus supporting regulatory phenomena with exeperimental evidences.

    Note that, we only provide the main details of each publication. The publication can then be consulted using the DOI or PMID.
    """
    serializer_class = serializers.PublicationDetailSerializer
    permission_classes = [permissions.SuperUserOrReadOnly]
    model = data.models.Publication
    fields = ['protrend_id', 'pmid', 'doi', 'title', 'author', 'year']
    targets = {'tfbs': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {}
