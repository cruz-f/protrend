from django.views import generic

from interfaces.website.forms import SearchForm


class IndexView(generic.TemplateView):
    views = ()
    template_name = "website/index.html"
    view_name = 'home'

    def get_context_data(self, **kwargs):
        # the view context
        # noinspection PyUnresolvedReferences
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm()
        context['active_page'] = 'home'
        return context
