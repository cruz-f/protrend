from collections import namedtuple
from typing import List, Type, Union

from django.urls import path
from django.views import generic
from rest_framework import generics, routers
from rest_framework.response import Response
from rest_framework.reverse import reverse


RoutedView = namedtuple(typename='RoutedView',
                        field_names=['prefix', 'list_view', 'detail_view'],
                        defaults=[None, None, None])


class IndexView(routers.APIRootView):
    """
    Index
    """
    views = ()

    def get(self, request, *args, **kwargs):
        data = {}

        for prefix, list_view, detail_view in self.views:
            view_name = f'{prefix}-list'
            data[prefix] = reverse(view_name, request=request)
        return Response(data)


class Router:
    index_class = IndexView

    def __init__(self,
                 route: str = None,
                 index: Type[generics.GenericAPIView, generic.View] = None,
                 name: str = None):
        """
        A router for class-based views.
        It allows registering both list and detail views into a single prefix.
        Then, dynamic URL paths will be reconstructed for each prefix according to the view type.
        In addition, a dynamic get view will be reconstructed for the main end-point of the router.
        An index end-point can be configured for the router.
        Otherwise, the end-point will be an empty string as it is common in django.

        :param: route - the index end-point
        :param: index - the index view
        :param: name - the name for the view
        """
        self._route = route
        self._index = index
        self._name = name
        self._views = []

    @property
    def route(self) -> str:
        if self._route is None:
            return ''

        return str(self._route)

    @property
    def index(self) -> Union[generic.View, routers.APIRootView]:
        if self._index:
            return self._index.as_view()

        self.index_class.views = self.views
        return self.index_class.as_view()

    @property
    def name(self) -> str:
        if self._name is None:
            return ''

        return str(self._name)

    @property
    def views(self) -> List[RoutedView]:
        return self._views.copy()

    @property
    def urls(self) -> List[path]:

        urls = [path(self.route, self.index, name=self.name)]

        for prefix, list_view, detail_view in self._views:

            if list_view is not None:
                url = path(f'{prefix}/', list_view.as_view(), name=f'{prefix}-list')
                urls.append(url)

            if detail_view is not None:
                url = path(f'{prefix}/<str:protrend_id>/', detail_view.as_view(), name=f'{prefix}-detail')
                urls.append(url)

        return urls

    def register(self,
                 prefix: str,
                 list_view: Type[generics.GenericAPIView] = None,
                 detail_view: Type[generics.GenericAPIView] = None):
        """
        Register either a list, detail or both views under a single prefix in this Router instance.

        :param: prefix - the prefix for the registered views
        :param: list_view - the list view
        :param: detail_view - the detail view
        """
        if prefix is None:
            raise ValueError('prefix is expecting a str type, but NoneType was passed')

        view = RoutedView(prefix=prefix, list_view=list_view, detail_view=detail_view)

        self._views.append(view)
