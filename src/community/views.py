from . import models
from .community_view_set import CommunityViewSet
from .forms import RegulatorForm, GeneForm


class RegulatorCommunityViewSet(CommunityViewSet):
    model = models.RegulatorCommunity
    form_class = RegulatorForm
    ordering = ['-protrend_id', '-locus_tag', 'uniprot_accession', '-name']
    list_display = ('protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'user')


class GeneCommunityViewSet(CommunityViewSet):
    model = models.GeneCommunity
    form_class = GeneForm
    ordering = ['-protrend_id', '-locus_tag', 'uniprot_accession', '-name']
    list_display = ('protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'user')