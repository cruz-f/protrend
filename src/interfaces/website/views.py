from django.shortcuts import render
from django.views import generic
from rest_framework import status

import domain.database as papi
import domain.model_api as mapi
import application.charts as charts
import application.tables as tables
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

        objs = context.pop('object_list')
        objs_dict = self.get_serialized_queryset(objs)
        context[self.context_object_name] = objs_dict

        # tables
        context[tables.OrganismsTable.context] = tables.OrganismsTable.context_dict()

        # charts
        org_regs = charts.OrganismsRegulatorsChart(objects=objs)
        context[org_regs.context] = org_regs.config

        top_chart = charts.OrganismsRegulatorsTopChart(objects=objs)
        context[top_chart.context] = top_chart.config

        taxa_chart = charts.OrganismsTaxaChart(objects=objs)
        context[taxa_chart.context] = taxa_chart.config

        ext_chart = charts.OrganismsExternalChart(objects=objs)
        context[ext_chart.context] = ext_chart.config

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
        context[tables.OrganismRegulatorsTable.context] = tables.OrganismRegulatorsTable.context_dict()
        context[tables.OrganismGenesTable.context] = tables.OrganismGenesTable.context_dict()
        context[tables.OrganismBindingsTable.context] = tables.OrganismBindingsTable.context_dict()
        context[tables.OrganismInteractionsTable.context] = tables.OrganismInteractionsTable.context_dict()

        # charts
        trn_chart = charts.OrganismTRNChart(objects=obj)
        context[trn_chart.context] = trn_chart.config

        regs_genes_chart = charts.OrganismRegulatorsGenesChart(objects=obj)
        context[regs_genes_chart.context] = regs_genes_chart.config

        genes_regs_chart = charts.OrganismGenesRegulatorsChart(objects=obj)
        context[genes_regs_chart.context] = genes_regs_chart.config

        # active page
        context['active_page'] = 'organisms'
        return context

    def get_serialized_queryset(self, queryset):
        return OrganismDetailSerializer(instance=queryset, context={'request': self.request}).data
