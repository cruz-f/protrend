from abc import abstractmethod
from typing import Union, List

from django.db.models import Model
from django_neomodel import DjangoNode
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings

import domain.database as papi
import interfaces.api.serializers as serializers
from exceptions import ProtrendException
from .permissions import SuperUserOrReadOnly


# --------------------------------------------
# BASE API VIEWS
# --------------------------------------------
class ObjectListCreateMixIn:
    """
    View to list and create ProTReND database objects.
    """
    @abstractmethod
    def get_queryset(self) -> Union[List[DjangoNode], List[Model]]:
        pass

    def get(self: Union['ObjectListCreateMixIn', generics.GenericAPIView], request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            Response({})

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self: Union['ObjectListCreateMixIn', generics.GenericAPIView], request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        error = self.perform_create(serializer)
        if error is not None:
            return Response(error.message, status=error.status)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def perform_create(serializer):
        try:
            serializer.save()
            return

        except ProtrendException as error:
            return error

    @staticmethod
    def get_success_headers(data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ObjectRetrieveUpdateDestroy:
    """
    View to retrieve, update and delete ProTReND database objects.
    """

    @abstractmethod
    def get_queryset(self, protrend_id: str) -> Union[DjangoNode, Model]:
        pass

    def get_object(self: Union['ObjectRetrieveUpdateDestroy', generics.GenericAPIView], protrend_id: str):
        obj = self.get_queryset(protrend_id)
        if obj is None:
            raise ProtrendException(detail='Object not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)

    def get(self: Union['ObjectRetrieveUpdateDestroy', generics.GenericAPIView],
            request,
            protrend_id: str,
            *args,
            **kwargs):
        obj = self.get_object(protrend_id)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def put(self: Union['ObjectRetrieveUpdateDestroy', generics.GenericAPIView],
            request,
            protrend_id: str,
            *args,
            **kwargs):
        partial = kwargs.pop('partial', False)
        obj = self.get_object(protrend_id)

        serializer = self.get_serializer(obj, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        error = self.perform_update(serializer)
        if error is not None:
            return Response(error.message, status=error.status)

        return Response(serializer.data)

    @staticmethod
    def perform_update(serializer):
        try:
            serializer.save()
            return

        except ProtrendException as error:
            return error

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.put(request, *args, **kwargs)

    def delete(self: Union['ObjectRetrieveUpdateDestroy', generics.GenericAPIView],
               request,
               protrend_id: str,
               *args,
               **kwargs):
        obj = self.get_object(protrend_id)
        serializer = self.get_serializer(obj)
        error = self.perform_destroy(serializer, obj)
        if error is not None:
            return Response(error.message, status=error.status)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def perform_destroy(serializer, obj):
        try:
            serializer.delete(obj)
            return

        except ProtrendException as error:
            return error


# --------------------------------------------
# CONCRETE API VIEWS
# --------------------------------------------
@api_view(['GET'])
def api_root(request):
    data = {'effectors': reverse('effector-list', request=request),
            'evidence': reverse('evidence-list', request=request)}
    return Response(data)


class EffectorList(ObjectListCreateMixIn, generics.GenericAPIView):
    serializer_class = serializers.EffectorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_effectors()


class EffectorDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    serializer_class = serializers.EffectorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_effector_by_id(protrend_id)


class EvidenceList(ObjectListCreateMixIn, generics.GenericAPIView):
    serializer_class = serializers.EvidenceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_evidences()


class EvidenceDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    serializer_class = serializers.EvidenceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_evidence_by_id(protrend_id)


class GeneList(ObjectListCreateMixIn, generics.GenericAPIView):
    serializer_class = serializers.GeneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_genes()


class GeneDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    serializer_class = serializers.GeneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_gene_by_id(protrend_id)


class OperonList(ObjectListCreateMixIn, generics.GenericAPIView):
    serializer_class = serializers.OperonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_operons()


class OperonDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    serializer_class = serializers.OperonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_operon_by_id(protrend_id)


class OrganismList(ObjectListCreateMixIn, generics.GenericAPIView):
    serializer_class = serializers.OrganismSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_organisms()


class OrganismDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    serializer_class = serializers.OrganismSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_organism_by_id(protrend_id)


class PathwayList(ObjectListCreateMixIn, generics.GenericAPIView):
    serializer_class = serializers.PathwaySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_pathways()


class PathwayDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    serializer_class = serializers.PathwaySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_pathway_by_id(protrend_id)


class PublicationList(ObjectListCreateMixIn, generics.GenericAPIView):
    serializer_class = serializers.PublicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_publications()


class PublicationDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    serializer_class = serializers.PublicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_publication_by_id(protrend_id)


class RegulatorList(ObjectListCreateMixIn, generics.GenericAPIView):
    serializer_class = serializers.RegulatorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_regulators()


class RegulatorDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    serializer_class = serializers.RegulatorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_regulator_by_id(protrend_id)


class RegulatoryFamilyList(ObjectListCreateMixIn, generics.GenericAPIView):
    serializer_class = serializers.RegulatoryFamilySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_rfams()


class RegulatoryFamilyDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    serializer_class = serializers.RegulatoryFamilySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_rfam_by_id(protrend_id)


class RegulatoryInteractionList(ObjectListCreateMixIn, generics.GenericAPIView):
    serializer_class = serializers.RegulatoryInteractionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_interactions()


class RegulatoryInteractionDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    serializer_class = serializers.RegulatoryInteractionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_interaction_by_id(protrend_id)


class TFBSList(ObjectListCreateMixIn, generics.GenericAPIView):
    serializer_class = serializers.TFBSSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_binding_sites()


class TFBSDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    serializer_class = serializers.TFBSSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_binding_site_by_id(protrend_id)
