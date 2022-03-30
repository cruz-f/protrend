import abc
from typing import Union, List, Dict

from django.views import generic
from django_neomodel import DjangoNode
from rest_framework import status

import domain.dpi as dpi
from application.charts.chart import Chart
from application.tables.table import Table
from domain.neo import NeoNode, NeoQuerySet, NeoLinkedQuerySet, NeoHyperLinkedQuerySet
from exceptions import ProtrendException


class GenericWebsiteView(metaclass=abc.ABCMeta):
    _context_objects_key = 'object'
    active_page = None
    serializer = None
    model = None
    fields = []
    targets = {}
    relationships = {}

    def get_context_data(self: Union['GenericWebsiteView', generic.ListView, generic.DetailView],
                         **kwargs):
        # the view context
        # noinspection PyUnresolvedReferences
        context = super().get_context_data(**kwargs)

        # the view objects
        objects = context.pop(self._context_objects_key)

        # the view serialized objects
        serialized_objects = self.get_serialized_objects(objects)
        context[self.context_object_name] = serialized_objects

        # tables
        tables = self.get_tables(objects)
        for table in tables:
            context[table.context] = table.context_dict()

        # charts
        charts = self.get_charts(objects)
        for chart in charts:
            context[chart.context] = chart.context_dict()

        # active page
        if self.active_page:
            context['active_page'] = self.active_page

        return context

    @abc.abstractmethod
    def get_queryset(self) -> Union[NeoQuerySet,
                                    NeoLinkedQuerySet,
                                    NeoHyperLinkedQuerySet]:
        pass

    @abc.abstractmethod
    def get_serialized_objects(self, objects: Union[List[DjangoNode], List[NeoNode], DjangoNode, NeoNode]) -> Dict:
        pass

    @abc.abstractmethod
    def get_tables(self, objects: Union[List[DjangoNode], List[NeoNode], DjangoNode, NeoNode]) -> List[Table]:
        pass

    @abc.abstractmethod
    def get_charts(self, objects: Union[List[DjangoNode], List[NeoNode], DjangoNode, NeoNode]) -> List[Chart]:
        pass


class WebsiteListView(GenericWebsiteView):
    """
    View to list ProTReND database objects.
    """
    _context_objects_key = 'object_list'

    def get_queryset(self: Union['WebsiteListView', generic.ListView]) -> Union[NeoQuerySet,
                                                                                NeoLinkedQuerySet,
                                                                                NeoHyperLinkedQuerySet]:
        return dpi.get_objects(cls=self.model,
                               fields=self.fields,
                               targets=self.targets,
                               relationships=self.relationships)

    def get_serialized_objects(self: Union['WebsiteListView', generic.ListView],
                               objects: Union[List[DjangoNode], List[NeoNode]]) -> Dict:
        return self.serializer(objects,
                               many=True,
                               context={'request': self.request}).data

    def get_tables(self, objects):
        return []

    def get_charts(self,objects):
        return []



class WebsiteDetailView(GenericWebsiteView):
    """
    Detail view for a ProTReND database object.
    """
    _context_objects_key = 'object'

    def get_queryset(self: Union['WebsiteDetailView', generic.DetailView]):
        return dpi.get_object(cls=self.model,
                              fields=self.fields,
                              targets=self.targets,
                              relationships=self.relationships,
                              **self.kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        objects = list(queryset)
        if not objects:
            raise ProtrendException(detail='Object not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)
        return objects[0]

    def get_serialized_objects(self: Union['WebsiteDetailView', generic.ListView],
                               objects: Union[List[DjangoNode], List[NeoNode]]) -> Dict:
        return self.serializer(objects,
                               context={'request': self.request}).data

    def get_tables(self, objects):
        return []

    def get_charts(self,objects):
        return []
