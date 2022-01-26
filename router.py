from collections import namedtuple
from typing import List, Type, Callable, Any, Union

from django.urls import path
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


RoutedView = namedtuple(typename='RoutedView',
                        field_names=['prefix', 'list_view', 'detail_view'],
                        defaults=[None, None, None])


class Router:

    def __init__(self, root: str = None):
        """
        A router for class-based views.
        It allows registering both list and detail views into a single prefix.
        Then, dynamic URL paths will be reconstructed for each prefix according to the view type.
        In addition, a dynamic get view will be reconstructed for the main end-point of the router.
        A root end-point can be configured for the router.
        Otherwise, the end-point will be an empty string as it is common in django.

        :param: root - the root end-point
        """
        if root is None:
            root = ''

        self._root = root
        self._views = []

    @property
    def root(self) -> Callable[[Any], Union[Response, Any]]:

        @api_view(['GET'])
        def _root(request):
            data = {}

            for prefix, list_view, detail_view in self._views:
                view_name = f'{prefix}-list'
                data[prefix] = reverse(view_name, request=request)
            return Response(data)

        return _root

    @property
    def views(self) -> List[RoutedView]:
        return self._views.copy()

    @property
    def urls(self):

        urls = [path(self._root, self.root)]

        for prefix, list_view, detail_view in self._views:

            if list_view is not None:
                url = path(prefix, list_view.as_view(), name=f'{prefix}-list')
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
