from functools import lru_cache
from typing import Type, List, Tuple, Union, TypeVar

from django_neomodel import DjangoNode
from neomodel import db

from domain.lazy import build_lazy_node, LazyNodeMeta
from set_list import SetList


def query_db(query: str) -> Tuple[List, List]:
    results, meta = db.cypher_query(query)
    meta = parse_meta(meta)
    return results, meta


def parse_meta(meta: List[str]) -> List[str]:
    parsed_meta = []
    for attr in meta:
        if '.' in attr:
            parsed_attr = attr.split('.')[1]
            parsed_meta.append(parsed_attr)

        else:
            parsed_meta.append(attr)

    return parsed_meta


class LazyQuerySet:

    def __init__(self, node: Type[DjangoNode], properties: List[str]):
        self.node = node
        self.properties = properties
        self.limit = 1
        self.skip = 0

    @property
    def node_label(self) -> str:
        return self.node.__label__

    @property
    def lower_node_label(self) -> str:
        return self.node_label.lower()

    @property
    @lru_cache()
    def lazy_node_cls(self) -> Union[type, LazyNodeMeta]:
        return build_lazy_node(self.node, self.properties)

    @property
    def lazy_query(self) -> str:
        query = f'MATCH ({self.lower_node_label}:{self.node_label}) RETURN '
        return_query = ', '.join(f'{self.lower_node_label}.{prop}' for prop in self.properties)
        final_query = query + return_query
        return final_query

    @property
    def count_query(self) -> str:
        return f'MATCH ({self.lower_node_label}:{self.node_label}) RETURN count({self.lower_node_label})'

    @property
    def skip_limit_lazy_query(self) -> str:
        skip = f' SKIP {int(self.skip)}'
        limit = f' LIMIT {int(self.limit)}'
        return self.lazy_query + skip + limit

    def parse_query_results(self, results: List[str], meta: List[str]) -> List[DjangoNode]:
        nodes = []
        for row in results:
            kwargs = {attr: val for attr, val in zip(meta, row)}
            lazy_node = self.lazy_node_cls(**kwargs)
            nodes.append(lazy_node)
        return nodes

    def all(self) -> List[DjangoNode]:
        results, meta = query_db(self.lazy_query)
        return self.parse_query_results(results, meta)

    def count(self) -> int:
        results, _ = query_db(self.count_query)
        return int(results[0][0])

    def __iter__(self):
        return (node for node in self.all())

    def __len__(self):
        results, _ = query_db(self.count_query)
        return int(results[0][0])

    def __bool__(self):
        return self.count() > 0

    def __nonzero__(self):
        return self.count() > 0

    def __contains__(self, obj):
        if not hasattr(obj, 'protrend_id'):
            raise ValueError('Expecting Protrend node saved instance')

        query = f'MATCH ({self.lower_node_label}:{self.node_label}) RETURN {self.lower_node_label}.protrend_id'
        results, meta = query_db(query)
        nodes = self.parse_query_results(results, meta)
        identifiers = [node.protrend_id for node in nodes]
        return obj.protrend_id in identifiers

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.stop and key.start:
                self.limit = key.stop - key.start
                self.skip = key.start
            elif key.stop:
                self.limit = key.stop
            elif key.start:
                self.skip = key.start

            results, meta = query_db(self.skip_limit_lazy_query)
            return self.parse_query_results(results, meta)

        elif isinstance(key, int):
            self.skip = key
            self.limit = 1

            results, meta = query_db(self.skip_limit_lazy_query)
            return self.parse_query_results(results, meta)[0]

        raise ValueError("Expecting slice or int")


T = TypeVar('T')


class NodeQuerySet(List[T]):

    def __init__(self, query_set=None, *args, **kwargs):
        super().__init__()
        self.query_set = query_set
        self.args = args
        self.kwargs = kwargs

    @property
    def data(self):
        if self.query_set is not None:
            data = self.query_set(*self.args, **self.kwargs)
            return list(data)

        return []

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __bool__(self):
        return len(self.data) > 0

    def __nonzero__(self):
        return len(self.data) > 0

    def __contains__(self, obj):
        if not hasattr(obj, 'protrend_id'):
            raise ValueError('Expecting Protrend node saved instance')

    def __getitem__(self, key):
        return self.data[key]


class UniqueNodeQuerySet(NodeQuerySet):

    @property
    def data(self):
        if self.query_set is not None:
            data = self.query_set(*self.args, **self.kwargs)
            return SetList(data)

        return []
