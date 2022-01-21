from typing import Type, Callable, List, Union

from django.db.models import Model
from django_neomodel import DjangoNode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .permissions import SuperUserOrReadOnly


class ObjectList:
    """
    View to list and create ProTReND database objects.
    """
    serializer_class: Type[Serializer] = None
    queryset: Callable = None
    permission_classes = [SuperUserOrReadOnly]

    def get_queryset(self) -> List[DjangoNode, Model]:
        return self.queryset()

    def get(self, request):
        objs = self.get_queryset()
        serializer = self.serializer_class(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectDetail:
    """
    View to retrieve, update and delete ProTReND database objects.
    """
    serializer_class: Type[Serializer] = None
    queryset: Callable = None
    permission_classes = [SuperUserOrReadOnly]

    def get_queryset(self, protrend_id) -> Union[DjangoNode, Model]:
        return self.queryset(protrend_id)

    def get_object(self, protrend_id):
        return self.get_queryset(protrend_id)

    def get(self, request, protrend_id):
        obj = self.get_object(protrend_id)
        if obj is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def put(self, request, protrend_id):
        obj = self.get_object(protrend_id)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, protrend_id):
        obj = self.get_object(protrend_id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
