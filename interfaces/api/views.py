from abc import abstractmethod
from typing import Type, List, Union

from django.db.models import Model
from django_neomodel import DjangoNode
from neomodel import NeomodelException
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.serializers import Serializer

import domain.database as papi
import interfaces.api.serializers as serializers
from .permissions import SuperUserOrReadOnly


# --------------------------------------------
# BASE API VIEWS
# --------------------------------------------
class ObjectList:
    """
    View to list and create ProTReND database objects.
    """
    serializer_class: Type[Serializer] = None
    permission_classes = [SuperUserOrReadOnly]

    @abstractmethod
    def get_queryset(self) -> Union[List[DjangoNode], List[Model]]:
        pass

    def get(self, request):
        objs = self.get_queryset()
        serializer = self.serializer_class(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except NeomodelException as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectDetail:
    """
    View to retrieve, update and delete ProTReND database objects.
    """
    serializer_class: Type[Serializer] = None
    permission_classes = [SuperUserOrReadOnly]

    @abstractmethod
    def get_queryset(self, protrend_id: str) -> Union[DjangoNode, Model]:
        pass

    def get_object(self, protrend_id: str):
        return self.get_queryset(protrend_id)

    def get(self, request, protrend_id: str):
        obj = self.get_object(protrend_id)
        if obj is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def put(self, request, protrend_id: str):
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


# --------------------------------------------
# CONCRETE API VIEWS
# --------------------------------------------
@api_view(['GET'])
def api_root(request):
    data = {'effectors': reverse('effector-list', request=request),
            'evidence': reverse('evidence-list', request=request)}
    return Response(data)


class EffectorList(ObjectList, generics.GenericAPIView):
    serializer_class = serializers.EffectorSerializer

    def get_queryset(self):
        return papi.get_effectors()


class EffectorDetail(ObjectDetail, generics.GenericAPIView):
    serializer_class = serializers.EffectorSerializer

    def get_queryset(self, protrend_id: str):
        return papi.get_effector_by_id(protrend_id)


class EvidenceList(ObjectList, generics.GenericAPIView):
    serializer_class = serializers.EvidenceSerializer

    def get_queryset(self):
        return papi.get_evidences()


class EvidenceDetail(ObjectDetail, generics.GenericAPIView):
    serializer_class = serializers.EvidenceSerializer

    def get_queryset(self, protrend_id: str):
        return papi.get_evidence_by_id(protrend_id)
