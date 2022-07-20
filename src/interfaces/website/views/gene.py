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


class GeneView(views.WebsiteDetailView, generic.DetailView):
    template_name = "website/gene.html"
    context_object_name = "gene"
    view_name = 'gene'

    active_page = ''
    serializer = serializers.GeneSerializer
    model = data.models.Gene
    fields = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms', 'function', 'description',
              'ncbi_gene', 'ncbi_protein', 'genbank_accession', 'refseq_accession', 'sequence',
              'strand', 'start', 'stop']
    targets = {'data_source': ['name', 'url'],
               'organism': ['protrend_id', 'name', 'species', 'strain', 'ncbi_taxonomy'],
               }
    relationships = {'data_source': ['external_identifier', 'url']}
