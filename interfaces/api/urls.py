from django.urls import path, include

from interfaces.api import views
from router import Router


# Create a router and register our class-based views.
router = Router()
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


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
