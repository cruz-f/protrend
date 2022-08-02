from django.urls import path, include
from django.views import generic

from . import views

urlpatterns = [
    path('', generic.RedirectView.as_view(url='./effector/'), name="index"),
    path('effector/', include(views.EffectorCommunityViewSet().urls)),
    path('gene/', include(views.GeneCommunityViewSet().urls)),
    path('interaciton/', include(views.InteractionCommunityViewSet().urls)),
    path('organism/', include(views.OrganismCommunityViewSet().urls)),
    path('regulator/', include(views.RegulatorCommunityViewSet().urls)),
    path('tfbs/', include(views.TFBSCommunityViewSet().urls)),
]
