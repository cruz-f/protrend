from abc import abstractmethod
from typing import Union

from neomodel import NodeSet
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.settings import api_settings

from domain import dpi
from domain.neo import NeoLinkedQuerySet, NeoQuerySet, NeoHyperLinkedQuerySet
from exceptions import ProtrendException
from utils import ExportFileMixin


def is_api(request) -> bool:
    if request.accepted_renderer.format == 'api':
        return True
    if request.query_params.get('page', False):
        return True

    return False


# --------------------------------------------
# BASE API VIEWS
# --------------------------------------------
class APIListView(ExportFileMixin):
    """
    View to list ProTReND database objects.
    """
    model = None
    fields = []

    def get_queryset(self):
        return dpi.get_objects(cls=self.model, fields=self.fields)

    # noinspection PyUnusedLocal
    def get(self: Union['APIListView', generics.GenericAPIView], request, *args, **kwargs):
        queryset = self.get_queryset()

        if is_api(request):
            page = self.paginate_queryset(queryset)

            if not page:
                return Response([{}], status=status.HTTP_204_NO_CONTENT)

            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        if not serializer.data:
            return Response([{}], status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.data)


class APICreateView:
    """
    View to list and create ProTReND database objects.
    """

    @abstractmethod
    def get_queryset(self) -> Union[None, NodeSet, NeoQuerySet, NeoLinkedQuerySet, NeoHyperLinkedQuerySet]:
        pass

    # noinspection PyUnusedLocal
    def post(self: Union['APICreateView', generics.GenericAPIView], request, *args, **kwargs):
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


class APIRetrieveView(ExportFileMixin):
    """
    View to retrieve ProTReND database objects.
    """
    model = None
    fields = []
    targets = {}
    relationships = {}

    def get_queryset(self: Union['APIRetrieveView', generics.GenericAPIView]):
        return dpi.get_object(cls=self.model,
                              fields=self.fields,
                              targets=self.targets,
                              relationships=self.relationships,
                              **self.kwargs)

    def get_object(self: Union['APIRetrieveView', generics.GenericAPIView]):
        queryset = self.get_queryset()
        objects = list(queryset)
        if not objects:
            raise ProtrendException(detail='Object not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)
        return objects[0]

    # noinspection PyUnusedLocal
    def get(self: Union['APIRetrieveView', generics.GenericAPIView],
            request,
            *args,
            **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class APIUpdateDestroyView:
    """
    View to retrieve, update and delete ProTReND database objects.
    """

    @abstractmethod
    def get_queryset(self) -> Union[None, NodeSet, NeoQuerySet, NeoLinkedQuerySet, NeoHyperLinkedQuerySet]:
        pass

    # noinspection PyUnusedLocal
    def put(self: Union['APIUpdateDestroyView', 'APIRetrieveView', generics.GenericAPIView],
            request,
            *args,
            **kwargs):
        partial = kwargs.pop('partial', False)
        obj = self.get_object()

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

    # noinspection PyUnusedLocal
    def delete(self: Union['APIUpdateDestroyView', 'APIRetrieveView', generics.GenericAPIView],
               request,
               *args,
               **kwargs):
        obj = self.get_object()
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
