from django.views import generic

import data
from application import tables, charts
from domain.neo import NeoLinkedQuerySet
from interfaces import views
from interfaces.website import serializers


class OrganismsView(views.WebsiteListView, generic.ListView):
    template_name = "website/organisms.html"
    context_object_name = "organisms"
    view_name = 'organisms'

    active_page = 'organisms'
    serializer = serializers.OrganismsSerializer
    model = data.models.Organism
    fields = ['protrend_id', 'name', 'ncbi_taxonomy',
              'species', 'refseq_accession', 'genbank_accession', 'assembly_accession']

    def get_tables(self, objects):
        return [tables.OrganismsTable()]

    def get_charts(self, objects):
        # performing a group_by_count in a linked query set is faster than obtaining a linked query set
        # at the instantiation of the view to retrieve all organisms and regulator objects
        queryset = NeoLinkedQuerySet(source=self.model,
                                     fields=['protrend_id'],
                                     target='regulator',
                                     target_fields=['protrend_id'])
        counts = queryset.group_by_count(field='name')
        return [charts.OrganismsRegulatorsChart(objects=counts),
                charts.OrganismsRegulatorsTopChart(objects=counts),
                charts.OrganismsTaxaChart(objects=objects),
                charts.OrganismsExternalChart(objects=objects)]


class OrganismView(views.WebsiteDetailView, generic.DetailView):
    template_name = "website/organism.html"
    context_object_name = "organism"
    view_name = 'organism'

    active_page = 'organisms'
    serializer = serializers.OrganismSerializer
    model = data.models.Organism
    fields = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain',
              'refseq_accession', 'refseq_ftp', 'genbank_accession',
              'genbank_ftp', 'ncbi_assembly', 'assembly_accession']
    targets = {'data_source': ['name', 'url'],
               'regulator': ['protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene'],
               'gene': ['protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene'],
               'tfbs': ['protrend_id', 'sequence', 'start', 'stop', 'strand'],
               'regulatory_interaction': ['protrend_id', 'organism', 'regulator', 'gene', 'tfbs', 'effector',
                                          'regulatory_effect']}
    relationships = {'data_source': ['external_identifier', 'url']}

    def get_tables(self, objects):
        return [tables.OrganismRegulatorsTable(),
                tables.OrganismGenesTable(),
                tables.OrganismBindingsTable(),
                tables.OrganismInteractionsTable()]

    def get_charts(self, objects):
        return [charts.OrganismTRNChart(objects=objects),
                charts.OrganismRegulatorsGenesChart(objects=objects),
                charts.OrganismGenesRegulatorsChart(objects=objects),
                charts.OrganismRegulatoryEffectChart(objects=objects)]
