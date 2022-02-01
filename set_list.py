from collections import UserList
from typing import Sequence, Any, Iterator, Union


class SetList(UserList):

    def __init__(self, sequence: Union[Iterator, Sequence] = None, key: str = 'protrend_id'):

        super().__init__()

        self.key = key

        if sequence is None:
            sequence = []

        self._add_elements(sequence)

    @property
    def keys(self):
        return [getattr(obj, self.key) for obj in self.data]

    def _add_element(self, element: Any):
        keys = self.keys
        if element not in keys:
            self.data.append(element)

    def _add_elements(self, sequence: Sequence):
        keys = self.keys

        for element in sequence:
            if element not in keys:
                self.data.append(element)

    def __setitem__(self, i, item):
        if item not in self.keys:
            self.data[i] = item

    def __delitem__(self, i):
        del self.data[i]

    def __add__(self, other: Sequence):

        new_instance = self.copy()
        new_instance.extend(other)

        return new_instance

    def __radd__(self, other: Sequence):

        new_instance = self.copy()
        new_instance.extend(other)

        return new_instance

    def __iadd__(self, other: Sequence):

        self._add_elements(other)

        return self

    def append(self, item):
        self._add_element(item)

    def insert(self, i, item):
        if item not in self.keys:
            self.data.insert(i, item)

    def copy(self) -> 'SetList':
        return self.__class__(self)

    def extend(self, other: Sequence):
        self._add_elements(other)

    def take_all(self):
        return self.data

    def take_first(self):
        if self.data:
            return self.data[0]

    def take_last(self):
        if self.data:
            return self.data[-1]
