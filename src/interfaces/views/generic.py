from abc import abstractmethod
from typing import Union, List

from django.db.models import Model
from django_neomodel import DjangoNode
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.settings import api_settings

from exceptions import ProtrendException
from utils import ExportFileMixin, get_header


# --------------------------------------------
# BASE API VIEWS
# --------------------------------------------
class ObjectListMixIn(ExportFileMixin):
    """
    View to list ProTReND database objects.
    """

    @abstractmethod
    def get_queryset(self, paginate: bool = False) -> Union[List[DjangoNode], List[Model]]:
        pass

    def get(self: Union['ObjectListMixIn', generics.GenericAPIView], request, *args, **kwargs):
        if request.accepted_renderer.format == 'api':
            queryset = self.get_queryset(paginate=True)
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            if not serializer.data:
                return Response([{}], status=status.HTTP_204_NO_CONTENT)

            return Response(serializer.data)

        queryset = self.get_queryset()
        if not queryset:
            return Response([{}], status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_renderer_context(self: Union['ObjectListMixIn', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        header = get_header(serializer_cls=serializer_cls)

        context['header'] = header
        return context


class ObjectCreateMixIn:
    """
    View to list and create ProTReND database objects.
    """

    @abstractmethod
    def get_queryset(self, paginate: bool = False) -> Union[List[DjangoNode], List[Model]]:
        pass

    def post(self: Union['ObjectCreateMixIn', generics.GenericAPIView], request, *args, **kwargs):
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


class ObjectRetrieveMixIn(ExportFileMixin):
    """
    View to retrieve ProTReND database objects.
    """

    @abstractmethod
    def get_queryset(self, protrend_id: str) -> Union[DjangoNode, Model]:
        pass

    def get_object(self: Union['ObjectRetrieveMixIn', generics.GenericAPIView], protrend_id: str):
        obj = self.get_queryset(protrend_id)
        if obj is None:
            raise ProtrendException(detail='Object not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)
        return obj

    def get(self: Union['ObjectRetrieveMixIn', generics.GenericAPIView],
            request,
            protrend_id: str,
            *args,
            **kwargs):
        obj = self.get_object(protrend_id)

        if request.accepted_renderer.format == 'api':
            serializer = self.get_serializer(obj)
            return Response(serializer.data)

        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def get_renderer_context(self: Union['ObjectRetrieveMixIn', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        header = get_header(serializer_cls=serializer_cls)

        context['header'] = header
        return context


class ObjectUpdateDestroyMixIn:
    """
    View to retrieve, update and delete ProTReND database objects.
    """

    @abstractmethod
    def get_queryset(self, protrend_id: str) -> Union[DjangoNode, Model]:
        pass

    def put(self: Union['ObjectUpdateDestroyMixIn', 'ObjectRetrieveMixIn', generics.GenericAPIView],
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

    def delete(self: Union['ObjectUpdateDestroyMixIn', 'ObjectRetrieveMixIn', generics.GenericAPIView],
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