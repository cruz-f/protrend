from typing import Union, List, Dict

import numpy as np
import pandas as pd
from django.views import generic
from django_neomodel import DjangoNode

import data
from application import tables, charts
from application.charts.chart import Chart
from application.sequences import make_motif_logo, make_motif_img, make_pwm
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

    def get_charts(self, objects: Union[List[DjangoNode], List[NeoNode]]) -> List[Chart]:
        # performing a group_by_count in a linked query set is faster than obtaining a linked query set
        # at the instantiation of the view to retrieve all organisms and regulator objects
        genes_queryset = NeoLinkedQuerySet(source=self.model,
                                           fields=['protrend_id'],
                                           target='gene',
                                           target_fields=['protrend_id'])
        genes_counts = genes_queryset.group_by_count()
        rfams_queryset = NeoLinkedQuerySet(source=data.RegulatoryFamily,
                                           fields=['name'],
                                           target='regulator',
                                           target_fields=['protrend_id'])
        rfams_counts = rfams_queryset.group_by_count()
        return [charts.RegulatorsGenesChart(objects=genes_counts),
                charts.RegulatorsGenesTopChart(objects=genes_counts),
                charts.RegulatoryFamiliesRegulatorsTopChart(objects=rfams_counts),
                charts.RegulatorsMechanismChart(objects=objects),
                charts.RegulatorsExternalChart(objects=objects)]


class RegulatorView(views.WebsiteDetailView, generic.DetailView):
    template_name = "website/regulator.html"
    context_object_name = "regulator"
    view_name = 'regulator'

    active_page = 'regulators'
    serializer = serializers.RegulatorSerializer
    model = data.Regulator
    fields = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms', 'function', 'description',
              'mechanism', 'ncbi_gene', 'ncbi_protein', 'genbank_accession', 'refseq_accession', 'sequence',
              'strand', 'start', 'stop']
    targets = {'data_source': ['name', 'url'],
               'organism': ['protrend_id', 'name', 'species', 'strain', 'ncbi_taxonomy'],
               'effector': ['protrend_id', 'name'],
               'pathway': ['protrend_id', 'name', 'kegg_pathways'],
               'gene': ['protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene'],
               'tfbs': ['protrend_id', 'sequence', 'start', 'stop', 'strand'],
               'regulatory_interaction': ['protrend_id', 'organism', 'regulator', 'gene', 'regulatory_effect'],
               'regulatory_family': ['protrend_id', 'name', 'mechanism', 'rfam', 'description']}
    relationships = {'data_source': ['external_identifier', 'url']}

    def get_tables(self, objects: Union[List[DjangoNode], List[NeoNode]]) -> List[Table]:
        return [tables.RegulatorEffectorsTable(),
                tables.RegulatorGenesTable(),
                tables.RegulatorBindingsTable(),
                tables.RegulatorInteractionsTable()]

    def get_charts(self, objects: Union[List[DjangoNode], List[NeoNode]]) -> List[Chart]:
        return [charts.RegulatorTRNChart(objects=objects),
                charts.RegulatorRegulatoryEffectChart(objects=objects)]

    @staticmethod
    def get_binding_motif(binding_sites: List[Dict]):
        sequences = [tfbs.get('sequence', '') for tfbs in binding_sites]
        pwm = make_pwm(sequences)
        logo = make_motif_logo(pwm)
        img = make_motif_img(logo)
        img = img.replace('height="180pt"', '').replace('width="720pt"', '')

        # split sequences
        sequences = np.array_split(sequences, 4)
        return pwm, sequences, img

    def get_context_data(self, **kwargs):
        context = super(RegulatorView, self).get_context_data(**kwargs)

        binding_sites = context[self.context_object_name].get('tfbs', [])

        if binding_sites:
            pwm, sequences, img = self.get_binding_motif(binding_sites)

            context['pwm'] = pwm
            context['motif_sequences'] = sequences
            context['motif'] = img

        else:
            context['pwm'] = pd.DataFrame()
            context['motif_sequences'] = []
            context['motif'] = '<svg height="30" width="200"><text x="0" y="15" fill="black">There is no motif available</text></svg>'

        return context
