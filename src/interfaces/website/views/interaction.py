from django.views import generic

import data
from interfaces import views
from interfaces.website import serializers


class InteractionView(views.WebsiteDetailView, generic.DetailView):
    template_name = "website/interaction.html"
    context_object_name = "interaction"
    view_name = 'interaction'

    active_page = ''
    serializer = serializers.RegulatoryInteractionSerializer
    model = data.models.RegulatoryInteraction
    fields = ['protrend_id', 'organism', 'effector', 'regulator', 'gene', 'tfbs', 'regulatory_effect']
    targets = {'data_source': ['name', 'url'],
               'data_organism': ['protrend_id', 'name', 'species', 'strain', 'ncbi_taxonomy'],
               'data_effector': ['protrend_id', 'name', 'kegg_compounds'],
               'data_regulator': ['protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'mechanism'],
               'data_gene': ['protrend_id', 'locus_tag', 'name', 'uniprot_accession'],
               'data_tfbs': ['protrend_id', 'sequence', 'start', 'stop', 'strand'],
               'evidence': ['protrend_id', 'name', 'description'],
               'publication': ['protrend_id', 'pmid', 'doi', 'title', 'author', 'year']}
    relationships = {'data_source': ['external_identifier', 'url']}
