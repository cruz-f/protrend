from . import models
from .community_view_set import CommunityViewSet
from .forms import RegulatorForm, GeneForm


class RegulatorCommunityViewSet(CommunityViewSet):
    model = models.RegulatorCommunity
    form_class = RegulatorForm
    ordering = ['-locus_tag', '-protrend_id', 'uniprot_accession', '-name']
    list_display = ('locus_tag', 'protrend_id', 'uniprot_accession', 'name', 'user')


class GeneCommunityViewSet(CommunityViewSet):
    model = models.GeneCommunity
    form_class = GeneForm
    ordering = ['-locus_tag', '-protrend_id', 'uniprot_accession', '-name']
    list_display = ('locus_tag', 'protrend_id', 'uniprot_accession', 'name', 'user')
