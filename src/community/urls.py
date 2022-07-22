from django.urls import path, include
from django.views import generic

from . import views

urlpatterns = [
    path('', generic.RedirectView.as_view(url='./effector/'), name="index"),
    path('effector/', include(views.EffectorCommunityViewSet().urls)),
    path('gene/', include(views.GeneCommunityViewSet().urls)),
    path('regulator/', include(views.RegulatorCommunityViewSet().urls)),
]
