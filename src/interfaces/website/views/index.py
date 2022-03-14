from django.shortcuts import render
from django.views import generic


class IndexView(generic.TemplateView):
    views = ()
    template_name = "website/index.html"
    view_name = 'home'


def fake_view(request, param=None):
    return render(request, "website/index.html", {'active_page': 'home'})
