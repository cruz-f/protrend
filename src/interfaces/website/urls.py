from django.contrib.auth.views import LogoutView
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
    # website main endpoints
    path(r'', include(router.urls)),
    path(r'about', views.about, name='about'),

    # search
    path(r'search', views.search, name='search'),

    # authentication
    path('activate/<uidb64>/<token>', website_views.activate, name='activate'),
    path('sign-in/', website_views.SignInView.as_view(), name="sign-in"),
    path("logout/", website_views.LogoutView.as_view(), name="logout"),
    path('sign-up/', website_views.sign_up, name="sign-up"),
    path('password-reset/', website_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', website_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', website_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', website_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # utils
    path(r'paginate-regulators', views.regulators_page, name='paginate-regulators'),
    path('utils/download-fasta/<str:identifier>/<str:locus_tag>/<str:name>/<str:sequence>',
         views.download_fasta, name='download-fasta')
]
