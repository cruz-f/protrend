from django.urls import path, include

from interfaces.website import views

import interfaces.website.views as website_views
from .router import WebsiteRouter

# Create a router and register our class-based views.
router = WebsiteRouter(r'')
router.register(r'organisms', list_view=website_views.OrganismsView, detail_view=website_views.OrganismView)
router.register(r'regulators', list_view=website_views.RegulatorsView, detail_view=website_views.RegulatorView)
router.register(r'genes', detail_view=website_views.GeneView)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'search', views.search, name='search'),
    path(r'paginate-regulators', views.regulators_page, name='paginate-regulators'),
    path(r'about', views.about, name='about'),
    # path('genes/<str:protrend_id>', views.fake_view, name='gene'),
    # path('binding-sites/<str:protrend_id>', views.fake_view, name='binding-site'),
    # path('interactions/<str:protrend_id>', views.fake_view, name='interaction'),
    # path('effectors/<str:protrend_id>', views.fake_view, name='effector'),
    path('utils/download-fasta/<str:identifier>/<str:locus_tag>/<str:name>/<str:sequence>',
         views.download_fasta, name='download-fasta')]
