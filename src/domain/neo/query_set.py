from functools import lru_cache
from itertools import groupby
from typing import Type, List, Union, Dict

from django_neomodel import DjangoNode

from .node import NodeMeta, node_factory
from .query import CYPHER_OPERATORS, query_meta, query_db


class NeoQuerySet:

    def __init__(self,
                 node: Type[DjangoNode],
                 fields: List[str] = None):

        if not fields:
            fields = ['protrend_id']

        self.node = node
        self.fields = fields
        self.limit = 1
        self.skip = 0
        self._data = None
        self._query = None

    @property
    def data(self):
        if self._data:
            return self._data

        if not self._query:
            self.all()

        results, meta = query_db(self._query)
        self._data = self.parse_query_results(results, meta)
        return self._data

    @property
    def label(self) -> str:
        return self.node.__label__

    @property
    def lower_label(self) -> str:
        return self.label.lower()

    @property
    @lru_cache()
    def node_cls(self) -> Union[type, NodeMeta]:
        return node_factory(fields=self.fields)

    @property
    def node_clause(self) -> str:
        return f'({self.lower_label}:{self.label})'

    @property
    def connection_clause(self) -> str:
        return '-[]->'

    @property
    def return_clause(self) -> str:
        fields_return = ', '.join(f'{self.lower_label}.{field}' for field in self.fields)
        return f'RETURN {fields_return}'

    @property
    def return_count_clause(self) -> str:
        return f'RETURN count({self.lower_label})'

    @property
    def skip_limit_clause(self) -> str:
        skip = f' SKIP {int(self.skip)}'
        limit = f' LIMIT {int(self.limit)}'
        return skip + limit

    @property
    def match_clause(self) -> str:
        return f'MATCH {self.node_clause}'

    @property
    def slice_query(self) -> str:
        return f'{self.match_clause} {self.return_clause} {self.skip_limit_clause}'

    def where_clause(self, **kwargs):
        where_clauses = []
        for key, value in kwargs.items():
            field, operator = key.split('__')
            left_operand = f'{self.lower_label}.{field}'
            right_operand = value

            operator = CYPHER_OPERATORS[operator]
            clause = operator(left_operand=left_operand, right_operand=right_operand)
            where_clauses.append(clause)

        where_clause = ' AND '.join(where_clauses)

        return f'WHERE {where_clause}'

    def parse_query_results(self, results: List[str], meta: List[str]) -> List[DjangoNode]:
        source_meta, _, _, _ = query_meta(meta, source_label=self.lower_label)

        nodes = []
        for row in results:
            kwargs = {attr: val for attr, val in zip(source_meta, row)}
            node_instance = self.node_cls(**kwargs)
            nodes.append(node_instance)

        return nodes

    def all(self):
        self._query = f'{self.match_clause} {self.return_clause}'
        return self

    def count(self) -> int:
        count_query = f'{self.match_clause} {self.return_count_clause}'
        results, _ = query_db(count_query)
        return int(results[0][0])

    def get(self, **kwargs):
        kwargs = {f'{key}__exact': value for key, value in kwargs.items()}
        return self.filter(**kwargs)

    def filter(self, **kwargs):
        where_clause = self.where_clause(**kwargs)
        self._query = f'{self.match_clause} {where_clause} {self.return_clause}'
        return self

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return self.count()

    def __bool__(self):
        return self.count() > 0

    def __nonzero__(self):
        return self.count() > 0

    def __contains__(self, obj):
        if not hasattr(obj, 'protrend_id'):
            raise ValueError('Expecting Protrend node saved instance')

        query = f'MATCH {self.node_clause} RETURN {self.lower_label}.protrend_id'
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

        elif isinstance(key, int):
            self.skip = key
            self.limit = 1

        else:
            raise ValueError("Expecting slice or int")

        results, meta = query_db(self.slice_query)
        results = self.parse_query_results(results, meta)

        if isinstance(key, int):
            return results[0]

        return results


class NeoLinkedQuerySet(NeoQuerySet):

    def __init__(self,
                 node: Type[DjangoNode],
                 fields: List[str] = None,
                 link: str = None,
                 link_fields: List[str] = None):

        super().__init__(node, fields)

        if not link:
            raise ValueError('Link cannot be empty for NeoLinkedQuerySets')

        if not link_fields:

            if link:
                link_fields = ['protrend_id']
            else:
                link_fields = []

        self.link = link
        self.link_fields = link_fields

    @property
    @lru_cache()
    def link_label(self) -> str:
        relationship = getattr(self.node, self.link)

        if 'node_class' not in relationship.definition:
            # noinspection PyProtectedMember
            relationship._lookup_node_class()

        return relationship.definition['node_class'].__label__

    @property
    def lower_link_label(self) -> str:
        return self.link_label.lower()

    @property
    @lru_cache()
    def node_cls(self) -> Union[type, NodeMeta]:
        return node_factory(fields=self.fields, link=self.link, link_fields=self.link_fields)

    @property
    def link_clause(self) -> str:
        return f'({self.lower_link_label}:{self.link_label})'

    @property
    def return_clause(self) -> str:
        node_return = ', '.join(f'{self.lower_label}.{field}' for field in self.fields)
        link_return = ', '.join(f'{self.lower_link_label}.{field}' for field in self.link_fields)
        return f'RETURN {node_return}, {link_return}'

    @property
    def return_count_clause(self) -> str:
        return f'RETURN {self.lower_label}.protrend_id, count({self.lower_link_label})'

    @property
    def match_clause(self) -> str:
        return f'MATCH {self.node_clause}{self.connection_clause}{self.link_clause}'

    @property
    def slice_query(self) -> str:
        return f'MATCH {self.node_clause} ' \
                f'WITH {self.lower_label} {self.skip_limit_clause} ' \
                f'MATCH ({self.lower_label}){self.connection_clause}{self.link_clause} ' \
                f'{self.return_clause}'

    def parse_query_results(self, results: List[str], meta: List[str]) -> List[DjangoNode]:
        source_meta, _, link_meta, key_fn = query_meta(meta,
                                                       source_label=self.lower_label,
                                                       rel_label='',
                                                       target_label=self.lower_link_label)

        n_source = len(source_meta)

        nodes = []

        results = sorted(results, key=key_fn)

        for fields, group in groupby(results, key_fn):
            kwargs = {attr: field for attr, field in zip(source_meta, fields)}

            values = list(group)

            link_kwargs = []
            for value in values:
                link_values = value[n_source:]
                link_kwarg = {attr: field for attr, field in zip(link_meta, link_values)}
                link_kwargs.append(link_kwarg)

            kwargs[self.link] = link_kwargs

            node_instance = self.node_cls(**kwargs)
            nodes.append(node_instance)

        return nodes

    def count(self) -> Dict[str, int]:
        count_query = f'{self.match_clause} {self.return_count_clause}'
        results, _ = query_db(count_query)

        def key_fn(x):
            return x[0]

        results = sorted(results, key=key_fn)

        nodes = {}
        for protrend_id, group in groupby(results, key_fn):
            group = list(zip(*group))
            count = group[1][0]
            nodes[protrend_id] = count
        return nodes

    def __len__(self):
        return super(NeoLinkedQuerySet, self).__len__()

    def __bool__(self):
        return super(NeoLinkedQuerySet, self).__bool__()

    def __nonzero__(self):
        return super(NeoLinkedQuerySet, self).__nonzero__()


class NeoHyperLinkedQuerySet(NeoLinkedQuerySet):

    def __init__(self,
                 node: Type[DjangoNode],
                 fields: List[str] = None,
                 link: str = None,
                 link_fields: List[str] = None,
                 rel_fields: List[str] = None):

        super().__init__(node=node,
                         fields=fields,
                         link=link,
                         link_fields=link_fields)

        if not rel_fields:
            raise ValueError('Relationship fields cannot be empty for NeoHyperLinkedQuerySet')

        self.rel_fields = rel_fields

    @property
    def rel_label(self):
        return 'rel_label'

    @property
    def connection_clause(self) -> str:
        return f'-[{self.rel_label}]->'

    @property
    def return_clause(self) -> str:
        node_return = ', '.join(f'{self.lower_label}.{field}' for field in self.fields)
        rel_return = ', '.join(f'{self.rel_label}.{field}' for field in self.rel_fields)
        link_return = ', '.join(f'{self.lower_link_label}.{field}' for field in self.link_fields)
        return f'RETURN {node_return}, {rel_return}, {link_return}'

    @property
    @lru_cache()
    def node_cls(self) -> Union[type, NodeMeta]:
        return node_factory(fields=self.fields, link=self.link, link_fields=self.link_fields)

    def parse_query_results(self, results: List[str], meta: List[str]) -> List[DjangoNode]:
        source_meta, rel_meta, link_meta, key_fn = query_meta(meta,
                                                              source_label=self.lower_label,
                                                              rel_label=self.rel_label,
                                                              target_label=self.lower_link_label)

        n_source = len(source_meta)
        n_source_rel = n_source + len(rel_meta)

        nodes = []

        results = sorted(results, key=key_fn)

        for fields, group in groupby(results, key_fn):
            kwargs = {attr: field for attr, field in zip(source_meta, fields)}

            values = list(group)

            link_kwargs = []
            for value in values:
                rel_values = value[n_source:n_source_rel]
                link_values = value[n_source_rel:]

                link_kwarg = {attr: field for attr, field in zip(link_meta, link_values)}
                rel_kwarg = {attr: field for attr, field in zip(rel_meta, rel_values)}
                link_kwarg['relationship'] = rel_kwarg
                link_kwargs.append(link_kwarg)

            kwargs[self.link] = link_kwargs

            node_instance = self.node_cls(**kwargs)
            nodes.append(node_instance)

        return nodes
