from functools import lru_cache
from itertools import groupby
from typing import Type, List, Union, Dict, Iterable

from django_neomodel import DjangoNode

from .node import NodeMeta, node_factory, BaseNode
from .query import CYPHER_OPERATORS, parse_query_meta, query_db


class NeoQuerySet:

    def __init__(self, source: Type[DjangoNode], fields: List[str] = None):

        if not fields:
            fields = ['protrend_id']
        else:
            if 'protrend_id' not in fields:
                fields.insert(0, 'protrend_id')

        self.source = source
        self.fields = fields
        self.limit = 1
        self.skip = 0
        self._data = []
        self._query = ''

    # -------------------------------------------------------------
    # BASE DYNAMIC PROPERTIES
    # -------------------------------------------------------------
    @property
    def query(self):
        if self._query:
            return self._query

        self.all()
        return self._query

    @property
    def data(self) -> List[BaseNode]:
        if self._data:
            return self._data

        return self.fetch()

    @property
    @lru_cache()
    def node_cls(self) -> Union[type, NodeMeta]:
        fields = getattr(self, 'fields', None)
        target = getattr(self, 'target', None)
        target_fields = getattr(self, 'target_fields', None)
        relationship_fields = getattr(self, 'relationship_fields', None)
        return node_factory(fields=fields,
                            target=target,
                            target_fields=target_fields,
                            relationship_fields=relationship_fields)

    # -------------------------------------------------------------
    # SOURCE PROPERTIES
    # -------------------------------------------------------------
    @property
    def source_label(self) -> str:
        return self.source.__label__

    @property
    def source_variable(self) -> str:
        return self.source_label.lower()

    @property
    def source_clause(self) -> str:
        return f'({self.source_variable}:{self.source_label})'

    @property
    def source_return(self) -> str:
        return ', '.join(f'{self.source_variable}.{field}' for field in self.fields)

    @property
    def count_source(self) -> str:
        return f'count({self.source_variable})'

    # -------------------------------------------------------------
    # BASE METHODS
    # -------------------------------------------------------------
    def copy(self) -> 'NeoQuerySet':
        instance = self.__class__.__new__(self.__class__)
        instance.__dict__.update(self.__dict__)
        return instance

    def fetch(self) -> List[BaseNode]:
        results, meta = query_db(self.query)
        data = self.parse(results=results, meta=meta)
        self._data = data
        return self._data

    # get method is only base to all query sets because it only calls the filter method, which is rather specific
    def get(self, **kwargs):
        kwargs = {f'{key}__exact': value for key, value in kwargs.items()}
        return self.filter(**kwargs)

    def __iter__(self) -> Iterable:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __bool__(self) -> bool:
        return len(self.data) > 0

    def __nonzero__(self) -> bool:
        return len(self.data) > 0

    def __contains__(self, obj) -> bool:
        if not hasattr(obj, 'protrend_id'):
            raise ValueError('Expecting Protrend source saved instance')

        for node in self:
            if node.protrend_id == obj.protrend_id:
                return True

        return False

    def _where_clauses(self, **kwargs):
        where_clauses = []
        for key, value in kwargs.items():
            field, operator = key.split('__')
            left_operand = f'{self.source_variable}.{field}'
            right_operand = value

            operator = CYPHER_OPERATORS[operator]
            clause = operator(left_operand=left_operand, right_operand=right_operand)
            where_clauses.append(clause)

        return where_clauses

    def _set_item(self, key):
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

    # -------------------------------------------------------------
    # SOURCE SPECIFIC/CUSTOM METHODS
    # -------------------------------------------------------------
    def parse(self, results: List[str], meta: List[str]) -> List[DjangoNode]:
        source_meta, _, _, _ = parse_query_meta(meta, source_variable=self.source_variable)

        nodes = []
        for row in results:
            kwargs = {attr: val for attr, val in zip(source_meta, row)}
            node_instance = self.node_cls(**kwargs)
            nodes.append(node_instance)

        return nodes

    def all(self):
        self._query = f'MATCH {self.source_clause} RETURN {self.source_return}'
        self._data = []
        return self

    def count(self) -> int:
        count_query = f'MATCH {self.source_clause} RETURN {self.count_source}'
        results, _ = query_db(count_query)
        return int(results[0][0])

    def filter(self, **kwargs):
        where_clauses = self._where_clauses(**kwargs)
        where_clause = ' AND '.join(where_clauses)

        if where_clause:
            self._query = f'MATCH {self.source_clause} WHERE {where_clause} RETURN {self.source_return}'
        else:
            self._query = f'MATCH {self.source_clause} RETURN {self.source_return}'

        self._data = []
        return self

    def __getitem__(self, key):
        self._set_item(key)

        skip = int(self.skip)
        limit = int(self.limit)
        query = f'MATCH {self.source_clause} RETURN {self.source_return} SKIP {skip} LIMIT {limit}'
        results, meta = query_db(query)
        data = self.parse(results=results, meta=meta)

        if isinstance(key, int):
            return data[key]

        return data


class NeoLinkedQuerySet(NeoQuerySet):

    def __init__(self,
                 source: Type[DjangoNode],
                 fields: List[str] = None,
                 target: str = None,
                 target_fields: List[str] = None):

        super().__init__(source, fields)

        if not target:
            raise ValueError('target cannot be empty for NeoLinkedQuerySets')

        if not target_fields:
            target_fields = ['protrend_id']
        else:
            if 'protrend_id' not in target_fields:
                target_fields.insert(0, 'protrend_id')

        self.target = target
        self.target_fields = target_fields

    # -------------------------------------------------------------
    # TARGET PROPERTIES
    # -------------------------------------------------------------
    @property
    @lru_cache()
    def target_label(self) -> str:
        relationship = getattr(self.source, self.target)

        if 'node_class' not in relationship.definition:
            # noinspection PyProtectedMember
            relationship._lookup_node_class()

        return relationship.definition['node_class'].__label__

    @property
    def target_variable(self) -> str:
        return self.target_label.lower()

    @property
    def target_clause(self) -> str:
        return f'({self.target_variable}:{self.target_label})'

    @property
    def target_return(self) -> str:
        return ', '.join(f'{self.target_variable}.{field}' for field in self.target_fields)

    @property
    def count_target(self) -> str:
        return f'count({self.target_variable})'

    # -------------------------------------------------------------
    # TARGET SPECIFIC/CUSTOM METHODS
    # -------------------------------------------------------------
    def parse(self, results: List[str], meta: List[str]) -> List[DjangoNode]:
        source_meta, _, link_meta, key_fn = parse_query_meta(meta,
                                                             source_variable=self.source_variable,
                                                             relationship_variable='',
                                                             target_variable=self.target_variable)

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

            kwargs[self.target] = link_kwargs

            node_instance = self.node_cls(**kwargs)
            nodes.append(node_instance)

        return nodes

    def all(self):
        self._query = f'MATCH {self.source_clause} ' \
                      f'OPTIONAL MATCH ({self.source_variable})-[]->{self.target_clause} ' \
                      f'RETURN {self.source_return}, {self.target_return}'
        self._data = []
        return self

    @staticmethod
    def _group_by_count(query: str):
        results, _ = query_db(query)

        def key_fn(x):
            return x[0]

        results = sorted(results, key=key_fn)

        nodes = {}
        for protrend_id, group in groupby(results, key_fn):
            group = list(zip(*group))
            count = group[1][0]
            nodes[protrend_id] = count
        return nodes

    def count(self) -> Dict[str, int]:
        query = f'MATCH {self.source_clause} ' \
                f'OPTIONAL MATCH ({self.source_variable})-[]->{self.target_clause} ' \
                f'RETURN {self.source_variable}.protrend_id, {self.count_target}'
        return self._group_by_count(query)

    def filter(self, **kwargs):
        where_clauses = self._where_clauses(**kwargs)
        where_clause = ' AND '.join(where_clauses)

        if where_clause:
            self._query = f'MATCH {self.source_clause} WHERE {where_clause} ' \
                          f'OPTIONAL MATCH ({self.source_variable})-[]->{self.target_clause} ' \
                          f'RETURN {self.source_return}, {self.target_return}'
        else:
            self._query = f'MATCH {self.source_clause} ' \
                          f'OPTIONAL MATCH ({self.source_variable})-[]->{self.target_clause} ' \
                          f'RETURN {self.source_return}, {self.target_return}'

        self._data = []
        return self

    def __getitem__(self, key):
        self._set_item(key)

        skip = int(self.skip)
        limit = int(self.limit)
        query = f'MATCH {self.source_clause} ' \
                f'WITH {self.source_variable} SKIP {skip} LIMIT {limit} ' \
                f'OPTIONAL MATCH ({self.source_variable})-[]->{self.target_clause} ' \
                f'RETURN {self.source_return}, {self.target_return}'
        results, meta = query_db(query)
        data = self.parse(results=results, meta=meta)

        if isinstance(key, int):
            return data[key]

        return data


class NeoHyperLinkedQuerySet(NeoLinkedQuerySet):

    def __init__(self,
                 source: Type[DjangoNode],
                 fields: List[str] = None,
                 target: str = None,
                 target_fields: List[str] = None,
                 relationship_fields: List[str] = None):

        super().__init__(source=source,
                         fields=fields,
                         target=target,
                         target_fields=target_fields)

        if not relationship_fields:
            raise ValueError('Relationship fields cannot be empty for NeoHyperLinkedQuerySet')

        self.relationship_fields = relationship_fields

    # -------------------------------------------------------------
    # RELATIONSHIP PROPERTIES
    # -------------------------------------------------------------
    @property
    def relationship_variable(self):
        return 'relationship_variable'

    @property
    def relationship_clause(self) -> str:
        return f'-[{self.relationship_variable}]->'

    @property
    def relationship_return(self) -> str:
        return ', '.join(f'{self.relationship_variable}.{field}' for field in self.relationship_fields)

    @property
    def count_relationship(self) -> str:
        return f'count({self.target_variable})'

    # -------------------------------------------------------------
    # TARGET SPECIFIC/CUSTOM METHODS
    # -------------------------------------------------------------
    def parse(self, results: List[str], meta: List[str]) -> List[DjangoNode]:
        source_meta, rel_meta, link_meta, key_fn = parse_query_meta(meta,
                                                                    source_variable=self.source_variable,
                                                                    relationship_variable=self.relationship_variable,
                                                                    target_variable=self.target_variable)

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

            kwargs[self.target] = link_kwargs

            node_instance = self.node_cls(**kwargs)
            nodes.append(node_instance)

        return nodes

    def all(self):
        self._query = f'MATCH {self.source_clause} ' \
                      f'OPTIONAL MATCH ({self.source_variable}){self.relationship_clause}{self.target_clause} ' \
                      f'RETURN {self.source_return}, {self.relationship_return}, {self.target_return}'
        self._data = []
        return self

    def count(self) -> Dict[str, int]:
        query = f'MATCH {self.source_clause} ' \
                f'OPTIONAL MATCH ({self.source_variable}){self.relationship_clause}{self.target_clause} ' \
                f'RETURN {self.source_variable}.protrend_id, {self.count_relationship}'

        return self._group_by_count(query)

    def filter(self, **kwargs):
        where_clauses = self._where_clauses(**kwargs)
        where_clause = ' AND '.join(where_clauses)

        if where_clause:
            self._query = f'MATCH {self.source_clause} WHERE {where_clause} ' \
                          f'OPTIONAL MATCH ({self.source_variable}){self.relationship_clause}{self.target_clause} ' \
                          f'RETURN {self.source_return}, {self.relationship_return}, {self.target_return}'
        else:
            self._query = f'MATCH {self.source_clause} ' \
                          f'OPTIONAL MATCH ({self.source_variable}){self.relationship_clause}{self.target_clause} ' \
                          f'RETURN {self.source_return}, {self.relationship_return}, {self.target_return}'

        self._data = []
        return self

    def __getitem__(self, key):
        self._set_item(key)

        skip = int(self.skip)
        limit = int(self.limit)
        query = f'MATCH {self.source_clause} ' \
                f'WITH {self.source_variable} SKIP {skip} LIMIT {limit} ' \
                f'OPTIONAL MATCH ({self.source_variable}){self.relationship_clause}{self.target_clause} ' \
                f'RETURN {self.source_return}, {self.relationship_return}, {self.target_return}'
        results, meta = query_db(query)
        data = self.parse(results=results, meta=meta)

        if isinstance(key, int):
            return data[key]

        return data


def add_query_sets(*query_sets: Union[NeoQuerySet,
                                      NeoLinkedQuerySet,
                                      NeoHyperLinkedQuerySet]) -> Union[NeoQuerySet,
                                                                        NeoLinkedQuerySet,
                                                                        NeoHyperLinkedQuerySet]:
    query_set = query_sets[0]

    data = {obj.protrend_id: obj for obj in query_set.data}
    for query_set_ in query_sets[1:]:

        for obj in query_set_.data:
            if obj.protrend_id in data:
                data_obj = data[obj.protrend_id]
                data_obj.add(obj)
            else:
                data[obj.protrend_id] = obj

    new_query_set = query_set.copy()
    new_query_set._data = list(data.values())
    return new_query_set
