from django.shortcuts import render
from django.views import generic
from rest_framework import status

import domain.database as papi
import domain.model_api as mapi
from application.table import (OrganismTable, OrganismRegulatorsTable, OrganismGenesTable, OrganismBindingsTable,
                               OrganismInteractionsTable)
from data import Organism
from exceptions import ProtrendException
from interfaces.serializers import OrganismQuery, OrganismDetailSerializer


def index(request):
    return render(request, "website/index.html", {'active_page': 'home'})


def fake_view(request, param=None):
    return render(request, "website/index.html", {'active_page': 'home'})


class OrganismsView(generic.ListView):
    template_name = "website/organisms.html"
    context_object_name = "organisms"

    def get_queryset(self):
        return papi.get_lazy_organisms_page()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context.pop('object_list')
        obj_dict = self.get_serialized_queryset(obj)
        context[self.context_object_name] = obj_dict

        # tables
        context[OrganismTable.context] = OrganismTable.context_dict()

        # active page
        context['active_page'] = 'organisms'
        return context

    def get_serialized_queryset(self, queryset):
        return OrganismQuery(instance=queryset, many=True).data


class OrganismView(generic.DetailView):
    template_name = "website/organism.html"
    context_object_name = "organism"
    pk_url_kwarg = 'protrend_id'

    def get_object(self, queryset=None):
        obj = mapi.get_object(cls=Organism, **self.kwargs)
        if obj is None:
            raise ProtrendException(detail='Object not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context.pop('object')
        obj_dict = self.get_serialized_queryset(obj)
        context[self.context_object_name] = obj_dict

        # tables
        context[OrganismRegulatorsTable.context] = OrganismRegulatorsTable.context_dict()
        context[OrganismGenesTable.context] = OrganismGenesTable.context_dict()
        context[OrganismBindingsTable.context] = OrganismBindingsTable.context_dict()
        context[OrganismInteractionsTable.context] = OrganismInteractionsTable.context_dict()

        # active page
        context['active_page'] = 'organisms'
        return context

    def get_serialized_queryset(self, queryset):
        return OrganismDetailSerializer(instance=queryset, context={'request': self.request}).data
