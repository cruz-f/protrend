from collections import namedtuple
from typing import List, Type

from django.urls import path
from rest_framework import generics


RoutedView = namedtuple(typename='RoutedView',
                        field_names=['prefix', 'list_view', 'detail_view'],
                        defaults=[None, None, None])


class Router:

    def __init__(self, api_root: generics.GenericAPIView):
        self._api_root = api_root
        self._views = []

    def register(self,
                 prefix: str,
                 list_view: Type[generics.GenericAPIView] = None,
                 detail_view: Type[generics.GenericAPIView] = None):
        if prefix is None:
            raise ValueError('prefix is expecting a str type, but NoneType was passed')

        view = RoutedView(prefix=prefix, list_view=list_view, detail_view=detail_view)

        self._views.append(view)

    @property
    def api_root(self) -> generics.GenericAPIView:
        return self._api_root

    @property
    def views(self) -> List[RoutedView]:
        return self._views.copy()

    @property
    def urls(self):

        urls = [path('', self.api_root)]

        for prefix, list_view, detail_view in self._views:

            if list_view is not None:
                url = path(prefix, list_view.as_view(), name=f'{prefix}-list')
                urls.append(url)

            if detail_view is not None:
                url = path(f'{prefix}/<str:protrend_id>/', detail_view.as_view(), name=f'{prefix}-detail')
                urls.append(url)

        return urls
