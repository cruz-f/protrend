from django.shortcuts import render
from django.views import generic


class IndexView(generic.TemplateView):
    views = ()
    template_name = "website/index.html"
    view_name = 'home'

    def get_context_data(self, **kwargs):
        # the view context
        # noinspection PyUnresolvedReferences
        context = super().get_context_data(**kwargs)

        context['active_page'] = 'home'
        return context


def fake_view(request, param=None):
    return render(request, "website/index.html", {'active_page': 'home'})
