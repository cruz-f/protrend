from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from .permissions import SuperUserOrReadOnly


class ObjectList(APIView):
    """
    List all objects and allows creating new ones.
    """
    serializer_class = Serializer
    query = None
    permission_classes = [SuperUserOrReadOnly]

    def get(self, request):
        objs = self.query()
        serializer = self.serializer_class(objs, many=True)
        return Response(serializer.data)

    # TODO: Try to fetch an equal record from the database.
    #  If there is no records infer the next protrend id and create node.
    #  Otherwise, raise an already exists error
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectDetail(APIView):
    """
    Retrieve, update or delete an object instance.
    """
    serializer_class = Serializer
    model = None
    query = None
    permission_classes = [SuperUserOrReadOnly]

    def get_object(self, protrend_id):
        try:
            return self.query(protrend_id)
        except self.model.DoesNotExist:
            raise Http404

    def get(self, request, protrend_id):
        obj = self.get_object(protrend_id)
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
