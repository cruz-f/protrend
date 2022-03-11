import rest_framework.permissions as drf_permissions
from rest_framework import generics

import data
from interfaces import views, permissions
from interfaces.api import serializers


class OrganismList(views.APIListView, views.APICreateView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Organisms available at ProTReND. Consult here the current list of all organisms in ProTReND.

    Organisms are listed in ProTReND by their scientific name and NCBI taxonomy identifier.

    Several details are available for each organism including the strain, the NCBI taxonomy identifier, GenBank, RefSeq and Assembly accessions for the reference genome associated with this organism.

    Note that the list of organisms available at ProTReND might contain redundant species due to the ambiguous scientific name found in the collected data sources and NCBI taxonomy misannotations.
    """
    serializer_class = serializers.OrganismListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Organism
    fields = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain']


class OrganismDetail(views.APIRetrieveView, views.APIUpdateDestroyView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Organisms available at ProTReND. Consult here all information available over this organism.

    Organisms are listed in ProTReND by their scientific name and NCBI taxonomy identifier.

    Several details are available for each organism including the strain, the NCBI taxonomy identifier, GenBank, RefSeq and Assembly accessions for the reference genome associated with this organism.

    Note that the list of organisms available at ProTReND might contain redundant species due to the ambiguous scientific name found in the collected data sources and NCBI taxonomy misannotations.
    """
    serializer_class = serializers.OrganismDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Organism
    fields = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain', 'refseq_accession', 'refseq_ftp',
              'genbank_accession', 'genbank_ftp', 'ncbi_assembly', 'assembly_accession']
    targets = {'data_source': ['name', 'url'],
               'regulator': ['protrend_id'],
               'gene': ['protrend_id'],
               'tfbs': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {'data_source': ['url']}
