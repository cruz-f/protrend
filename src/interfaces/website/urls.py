from django.urls import path

from interfaces.website import views

urlpatterns = [path(r'', views.index, name='home'),
               path('organisms', views.OrganismsView.as_view(), name='organisms'),
               path('organisms/<str:protrend_id>', views.OrganismView.as_view(), name='organism'),
               path('regulators/<str:protrend_id>', views.fake_view, name='regulator'),
               path('genes/<str:protrend_id>', views.fake_view, name='gene'),
               path('bindings/<str:protrend_id>', views.fake_view, name='binding'),
               path('interactions/<str:protrend_id>', views.fake_view, name='interaction')]
