from typing import List

from django.urls import path

from interfaces.website.views.index import IndexView
from router import Router


class WebsiteRouter(Router):
    """
    Custom Website Router
    """
    index_class = IndexView

    @property
    def urls(self) -> List[path]:

        urls = [path(self.route, self.index, name=self.index_class.view_name)]

        for prefix, list_view, detail_view in self._views:

            if list_view is not None:
                url = path(f'{prefix}/', list_view.as_view(), name=list_view.view_name)
                urls.append(url)

            if detail_view is not None:
                url = path(f'{prefix}/<str:protrend_id>/', detail_view.as_view(), name=detail_view.view_name)
                urls.append(url)

        return urls
