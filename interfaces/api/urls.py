from django.urls import path

from interfaces.api import views

urlpatterns = [
    path('', views.api_root),
    path('effectors/', views.EffectorList.as_view(), name='effector-list'),
    path('effectors/<str:protrend_id>/', views.EffectorDetail.as_view(), name='effector-detail'),
    path('evidences/', views.EvidenceList.as_view(), name='evidence-list'),
    path('evidences/<str:protrend_id>/', views.EvidenceDetail.as_view(), name='evidence-detail'),
]
