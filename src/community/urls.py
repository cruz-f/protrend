from django.urls import path, include
from django.views import generic

from .views import RegulatorCommunityViewSet, GeneCommunityViewSet

urlpatterns = [
    path('', generic.RedirectView.as_view(url='./regulator/'), name="index"),
    path('regulator/', include(RegulatorCommunityViewSet().urls)),
    path('gene/', include(GeneCommunityViewSet().urls)),
]
