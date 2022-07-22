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
    list_display = ('id', 'locus_tag', 'protrend_id', 'uniprot_accession', 'name', 'user')


class RegulatorCommunityViewSet(CommunityViewSet):
    model = models.RegulatorCommunity
    form_class = forms.RegulatorForm
    ordering = ['-id']
    list_display = ('id', 'locus_tag', 'protrend_id', 'uniprot_accession', 'name', 'user')
