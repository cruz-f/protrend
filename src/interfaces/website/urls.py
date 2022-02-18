from django.urls import path

from interfaces.website import views

urlpatterns = [path(r'', views.index, name='home')]
