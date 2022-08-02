from .community_view_set import CommunityViewSet
from . import models
from . import forms


class EffectorCommunityViewSet(CommunityViewSet):
    model = models.EffectorCommunity
    form_class = forms.EffectorForm
    ordering = ['-id']
    list_display = ('id', 'name', 'protrend_id', 'user')


class GeneCommunityViewSet(CommunityViewSet):
    model = models.GeneCommunity
    form_class = forms.GeneForm
    ordering = ['-id']
    list_display = ('id', 'locus_tag', 'name', 'uniprot_accession', 'protrend_id', 'user')


class InteractionCommunityViewSet(CommunityViewSet):
    model = models.InteractionCommunity
    form_class = forms.InteractionForm
    ordering = ['-id']
    list_display = ('id', 'organism', 'regulator', 'gene', 'tfbs', 'effector', 'protrend_id', 'user')


class OrganismCommunityViewSet(CommunityViewSet):
    model = models.OrganismCommunity
    form_class = forms.OrganismForm
    ordering = ['-id']
    list_display = ('id', 'name', 'ncbi_taxonomy', 'refseq_accession', 'genbank_accession', 'protrend_id', 'user')


class RegulatorCommunityViewSet(CommunityViewSet):
    model = models.RegulatorCommunity
    form_class = forms.RegulatorForm
    ordering = ['-id']
    list_display = ('id', 'locus_tag', 'name', 'uniprot_accession', 'protrend_id', 'protrend_id', 'user')


class TFBSCommunityViewSet(CommunityViewSet):
    model = models.TFBSCommunity
    form_class = forms.TFBSForm
    ordering = ['-id']
    list_display = ('id', 'sequence', 'strand', 'start', 'stop', 'protrend_id', 'user')
