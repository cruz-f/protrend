from collections import UserList
from typing import Sequence, Any, Iterator, Union, List, TypeVar


T = TypeVar('T')


class SetList(UserList, List[T]):

    def __init__(self, sequence: Union[Iterator, Sequence] = None, key: str = 'protrend_id'):
        if sequence is None:
            sequence = []

        super().__init__()

        self._unique = []
        self.key = key

        for element in sequence:
            self._add_element(element)

    def _get_element_key(self, element: Any):
        if self.key:
            return getattr(element, self.key)

        hash(element)
        return element

    def _add_element(self, element: Any):
        key = self._get_element_key(element)

        if key not in self._unique:
            self._unique.append(key)
            self.data.append(element)

    def _insert_element(self, i: int, element: Any):
        key = self._get_element_key(element)

        if key not in self._unique:
            self._unique[i] = element
            self.data[i] = element

    def __setitem__(self, i, item):
        self._insert_element(i, item)

    def __delitem__(self, i):
        del self._unique[i]
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
        self.extend(other)
        return self

    def append(self, item):
        self._add_element(item)

    def insert(self, i, item):
        self._insert_element(i, item)

    def copy(self) -> 'SetList':
        return self.__class__(self)

    def extend(self, other: Sequence):
        for element in other:
            self._add_element(element)
