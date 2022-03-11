from abc import ABCMeta, abstractmethod
from typing import Union, Any, List


class Chart(metaclass=ABCMeta):
    _chart_type = 'bar'
    _responsive = True
    _aspect_ratio = False
    _orientation = 'vertical'
    _legend = 'top'
    _title = 'ProTRenD'
    _x_label = None
    _y_label = None

    def __init__(self, objects: Union[Any, List[Any]]):
        self.objects = objects

    @property
    def context(self):
        return f'{self.__class__.__name__}Data'

    @property
    def type_(self):
        return {'type': self._chart_type}

    @property
    def options(self):
        plugins = {}
        if self._legend:
            plugins['legend'] = {'position': self._legend}

        if self._title:
            plugins['title'] = {'display': True, 'text': self._title}

        scales = {}
        if self._x_label:
            scales['x'] = {'display': True,
                           'title': {'display': True, 'text': self._x_label}}

        if self._y_label:
            scales['y'] = {'display': True,
                           'title': {'display': True, 'text': self._y_label}}

        if self._orientation == 'vertical':
            return {'options': {'responsive': self._responsive,
                                'maintainAspectRatio': self._aspect_ratio,
                                'scales': scales,
                                'plugins': plugins}}

        return {'options': {'responsive': self._responsive,
                            'maintainAspectRatio': self._aspect_ratio,
                            'indexAxis': 'y',
                            'scales': scales,
                            'plugins': plugins}}

    @property
    @abstractmethod
    def data(self):
        pass

    @property
    def config(self):
        return {**self.type_,
                **self.options,
                **self.data}

    def context_dict(self):
        return self.config
