from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import rest_framework.permissions as drf_permissions


import interfaces.api.views as api_views
import interfaces.permissions as permissions
from .router import APIRouter


# Create a router and register our class-based views.
router = APIRouter(r'', name='api')
router.register(r'effectors', list_view=api_views.EffectorList, detail_view=api_views.EffectorDetail)
router.register(r'evidences', list_view=api_views.EvidenceList, detail_view=api_views.EvidenceDetail)
router.register(r'genes', list_view=api_views.GeneList, detail_view=api_views.GeneDetail)
router.register(r'operons', list_view=api_views.OperonList, detail_view=api_views.OperonDetail)
router.register(r'organisms', list_view=api_views.OrganismList, detail_view=api_views.OrganismDetail)
router.register(r'pathways', list_view=api_views.PathwayList, detail_view=api_views.PathwayDetail)
router.register(r'publications', list_view=api_views.PublicationList, detail_view=api_views.PublicationDetail)
router.register(r'regulators', list_view=api_views.RegulatorList, detail_view=api_views.RegulatorDetail)
router.register(r'rfams', list_view=api_views.RegulatoryFamilyList, detail_view=api_views.RegulatoryFamilyDetail)
router.register(r'interactions', list_view=api_views.InteractionsList, detail_view=api_views.InteractionDetail)
router.register(r'binding-sites', list_view=api_views.BindingSitesList, detail_view=api_views.BindingSiteDetail)
router.register(r'trns', list_view=api_views.TRNs, detail_view=api_views.TRN)
router.register(r'organisms-binding-sites', list_view=api_views.OrganismsBindingSites,
                detail_view=api_views.OrganismBindingSites)
router.register(r'regulators-binding-sites', list_view=api_views.RegulatorsBindingSites,
                detail_view=api_views.RegulatorBindingSites)


schema_view = get_schema_view(
    openapi.Info(
        title="ProTReND REST API",
        default_version='v1',
        description="ProTReND provides open programmatic access to the Transcriptional Regulatory Network (TRN) database through a RESTful web API",
        terms_of_service="",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly),
)


# The API URLs are now determined automatically by the router.
# noinspection PyUnresolvedReferences
urlpatterns = [
    path('', include(router.urls)),
    path(r'best-practices/', api_views.best_practices, name='best-practices'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
