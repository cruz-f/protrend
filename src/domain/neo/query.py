from typing import List, Tuple

from neomodel import db


def cypher_closure(operator, quotation=False, takes_operand=True):

    def wrapper(left_operand=None, right_operand=None):
        if not takes_operand:
            return f"{left_operand} {operator}"

        if quotation:
            return f"{left_operand} {operator} '{right_operand}'"

        return f"{left_operand} {operator} {right_operand}"

    return wrapper


CYPHER_OPERATORS = {'exact': cypher_closure(operator='=', quotation=True),
                    'ne': cypher_closure(operator='!=', quotation=True),
                    'lt': cypher_closure(operator='<'),
                    'gt': cypher_closure(operator='>'),
                    'lte': cypher_closure(operator='<='),
                    'gte': cypher_closure(operator='>='),
                    'in': cypher_closure(operator='in'),
                    'isnull': cypher_closure(operator='IS NULL', takes_operand=False),
                    'contains': cypher_closure(operator='CONTAINS'),
                    'startswith': cypher_closure(operator='STARTS WITH', quotation=True),
                    'endswith': cypher_closure(operator='ENDS WITH', quotation=True)}


def query_db(query: str) -> Tuple[List[str], List[str]]:
    return db.cypher_query(query)


def parse_query_meta(meta, source_variable='', relationship_variable='', target_variable=''):
    source_meta = []
    relationship_meta = []
    target_meta = []

    for key in meta:
        variable, field = key.split('.')
        if variable == source_variable:
            source_meta.append(field)
        elif variable == relationship_variable:
            relationship_meta.append(field)
        elif variable == target_variable:
            target_meta.append(field)
        else:
            continue

    def key_fn(x):
        return tuple([x[i] for i, _ in enumerate(source_meta)])

    return source_meta, relationship_meta, target_meta, key_fn
