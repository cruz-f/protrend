from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from interfaces.api.permissions import SuperUserOrReadOnly
from interfaces.api.router import APIRouter
from interfaces.api import views


# Create a router and register our class-based views.
router = APIRouter(r'', name='api')
router.register(r'effectors', list_view=views.EffectorList, detail_view=views.EffectorDetail)
router.register(r'evidences', list_view=views.EvidenceList, detail_view=views.EvidenceDetail)
router.register(r'genes', list_view=views.GeneList, detail_view=views.GeneDetail)
router.register(r'operons', list_view=views.OperonList, detail_view=views.OperonDetail)
router.register(r'organisms', list_view=views.OrganismList, detail_view=views.OrganismDetail)
router.register(r'pathways', list_view=views.PathwayList, detail_view=views.PathwayDetail)
router.register(r'publications', list_view=views.PublicationList, detail_view=views.PublicationDetail)
router.register(r'regulators', list_view=views.RegulatorList, detail_view=views.RegulatorDetail)
router.register(r'rfams', list_view=views.RegulatoryFamilyList, detail_view=views.RegulatoryFamilyDetail)
router.register(r'interactions', list_view=views.RegulatoryInteractionList,
                detail_view=views.RegulatoryInteractionDetail)
router.register(r'binding-sites', list_view=views.TFBSList, detail_view=views.TFBSDetail)
router.register(r'trns', list_view=views.TRNList, detail_view=views.TRNDetail)


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
    permission_classes=(permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly),
)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path(r'best-practices/', views.best_practices, name='best-practices'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
