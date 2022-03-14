from typing import Union, List

from django.views import generic
from django_neomodel import DjangoNode

import data
from application import tables, charts
from application.charts.chart import Chart
from application.tables.table import Table
from domain.neo import NeoNode, NeoLinkedQuerySet
from interfaces import views
from interfaces.website import serializers


class RegulatorsView(views.WebsiteListView, generic.ListView):
    template_name = "website/regulators.html"
    context_object_name = "regulators"
    view_name = 'regulators'

    active_page = 'regulators'
    serializer = serializers.RegulatorsSerializer
    model = data.Regulator
    fields = ['protrend_id', 'locus_tag', 'name', 'mechanism',
              'uniprot_accession', 'ncbi_gene', 'ncbi_protein', 'genbank_accession', 'refseq_accession']

    def get_tables(self, objects: Union[List[DjangoNode], List[NeoNode]]) -> List[Table]:
        return [tables.RegulatorsTable()]

    def get_charts(self, objects: Union[List[DjangoNode], List[NeoNode]]) -> List[Chart]:
        # performing a group_by_count in a linked query set is faster than obtaining a linked query set
        # at the instantiation of the view to retrieve all organisms and regulator objects
        queryset = NeoLinkedQuerySet(source=self.model,
                                     fields=['protrend_id'],
                                     target='gene',
                                     target_fields=['protrend_id'])
        counts = queryset.group_by_count()
        return []


class RegulatorView(views.WebsiteDetailView, generic.DetailView):
    template_name = "website/regulator.html"
    context_object_name = "regulator"
    view_name = 'regulator'

    active_page = 'regulators'
    serializer = serializers.RegulatorSerializer
    model = data.Regulator
    fields = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain',
              'refseq_accession', 'refseq_ftp', 'genbank_accession',
              'genbank_ftp', 'ncbi_assembly', 'assembly_accession']
    targets = {'data_source': ['name', 'url'],
               'regulator': ['protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene'],
               'gene': ['protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene'],
               'tfbs': ['protrend_id', 'sequence', 'start', 'stop', 'strand'],
               'regulatory_interaction': ['protrend_id', 'regulator', 'gene', 'regulatory_effect']}
    relationships = {'data_source': ['external_identifier', 'url']}

    def get_tables(self, objects: Union[List[DjangoNode], List[NeoNode]]) -> List[Table]:
        return []

    def get_charts(self, objects: Union[List[DjangoNode], List[NeoNode]]) -> List[Chart]:
        return []
