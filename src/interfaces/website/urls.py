from django.urls import path, include

from interfaces.website import views

import interfaces.website.views as website_views
from .router import WebsiteRouter


# Create a router and register our class-based views.
router = WebsiteRouter(r'')
router.register(r'organisms', list_view=website_views.OrganismsView, detail_view=website_views.OrganismView)

urlpatterns = [
    path(r'', include(router.urls)),
    path('regulators/<str:protrend_id>', views.fake_view, name='regulator'),
    path('genes/<str:protrend_id>', views.fake_view, name='gene'),
    path('bindings/<str:protrend_id>', views.fake_view, name='binding'),
    path('interactions/<str:protrend_id>', views.fake_view, name='interaction')]
