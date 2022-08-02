from django.views import generic

import data
from interfaces import views
from interfaces.website import serializers


class GeneView(views.WebsiteDetailView, generic.DetailView):
    template_name = "website/gene.html"
    context_object_name = "gene"
    view_name = 'gene'

    active_page = ''
    serializer = serializers.GeneSerializer
    model = data.models.Gene
    fields = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms', 'function', 'description',
              'ncbi_gene', 'ncbi_protein', 'genbank_accession', 'refseq_accession', 'gene_sequence', 'protein_sequence',
              'strand', 'start', 'stop']
    targets = {'data_source': ['name', 'url'],
               'organism': ['protrend_id', 'name', 'species', 'strain', 'ncbi_taxonomy'],
               'operon': ['protrend_id', 'operon_db_id', 'name', 'function', 'genes']}
    relationships = {'data_source': ['external_identifier', 'url']}
