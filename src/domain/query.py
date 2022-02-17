from typing import Type, List, Tuple

from django_neomodel import DjangoNode
from neomodel import db

from domain.lazy import build_lazy_node


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


def parse_query_results(node: Type[DjangoNode], results: List, meta: List = None) -> List[DjangoNode]:
    cls = build_lazy_node(node=node, meta=meta)

    nodes = []
    for row in results:
        kwargs = {attr: val for attr, val in zip(meta, row)}
        instance = cls(**kwargs)
        nodes.append(instance)
    return nodes


def build_lazy_query(node: Type[DjangoNode], properties: List[str]) -> str:
    label = node.__label__
    lower_label = node.__label__.lower()
    query = f'MATCH ({lower_label}:{label}) RETURN '
    return_query = ', '.join(f'{lower_label}.{prop}' for prop in properties)
    final_query = query + return_query
    return final_query


def build_identifiers_query(node: Type[DjangoNode]) -> str:
    return build_lazy_query(node, ['protrend_id'])
