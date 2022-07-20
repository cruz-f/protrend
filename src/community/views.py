from material.frontend.views import ModelViewSet

from . import models
from .forms import RegulatorForm, GeneForm
from .permissions import CommunityPermissionsMixIn


class RegulatorCommunityViewSet(CommunityPermissionsMixIn, ModelViewSet):
    model = models.RegulatorCommunity
    form_class = RegulatorForm
    ordering = ['-locus_tag', 'uniprot_accession', '-name']
    list_display = ('locus_tag', 'uniprot_accession', 'name', 'user')


class GeneCommunityViewSet(CommunityPermissionsMixIn, ModelViewSet):
    model = models.GeneCommunity
    form_class = GeneForm
    ordering = ['-locus_tag', 'uniprot_accession', '-name']
    list_display = ('locus_tag', 'uniprot_accession', 'name', 'user')
