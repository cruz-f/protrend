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
        return self.get_queryset(protrend_id)

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
