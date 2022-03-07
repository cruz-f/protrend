from typing import Union, Type, List, Dict

from django_neomodel import DjangoNode

from .utils import raise_exception
from ..neo import BaseNode, NeoQuerySet, node_factory, NeoLinkedQuerySet, NeoHyperLinkedQuerySet


_model_type = Union[Type[DjangoNode], Type[BaseNode]]
_model = Union[DjangoNode, BaseNode]


def get_query_set(cls: _model_type,
                  fields: List[str] = None,
                  link: str = None,
                  link_fields: List[str] = None,
                  rel_fields: List[str] = None) -> Union[NeoQuerySet, NeoLinkedQuerySet, NeoHyperLinkedQuerySet]:
    if not link:
        return NeoQuerySet(node=cls, fields=fields)

    if not rel_fields:
        return NeoLinkedQuerySet(node=cls, fields=fields, link=link, link_fields=link_fields)

    return NeoHyperLinkedQuerySet(node=cls, fields=fields, link=link, link_fields=link_fields)


# ---------------------------------------------------------
# Bulk Object Queries
# ---------------------------------------------------------
@raise_exception
def get_objects(cls: _model_type,
                fields: List[str] = None,
                link: str = None,
                link_fields: List[str] = None,
                rel_fields: List[str] = None) -> Union[None, NeoQuerySet, NeoLinkedQuerySet, NeoHyperLinkedQuerySet]:
    """
    Get all objects from the database of a given node type.
    If a link is requested,
    the link/relationship fields will be also retrieved from all objects related with each single object
    """
    query_set = get_query_set(cls=cls, fields=fields, link=link, link_fields=link_fields, rel_fields=rel_fields)
    return query_set.all()


@raise_exception
def get_identifiers(cls: _model_type, link: str = None) -> Union[None, NeoQuerySet, NeoLinkedQuerySet, NeoHyperLinkedQuerySet]:
    """
    Get all objects identifiers from the database of a given node type.
    If a link is requested,
    the link/relationship identifiers will be also retrieved from all objects related with each single object
    """
    if link:
        query_set = NeoLinkedQuerySet(node=cls, fields=['protrend_id'], link=link, link_fields=['protrend_id'])
    else:
        query_set = NeoQuerySet(node=cls)
    return query_set.all()


@raise_exception
def count_objects(cls: _model_type, link: str = None) -> Union[int, Dict[str, int]]:
    """
    Count all objects from the database of a given node type.
    If a link is requested,
    the link/relationship fields will be also retrieved from all objects related with each single object
    """
    if link:
        query_set = NeoLinkedQuerySet(node=cls, fields=['protrend_id'], link=link, link_fields=['protrend_id'])
    else:
        query_set = NeoQuerySet(node=cls)

    return query_set.count()


@raise_exception
def filter_objects(cls: _model_type,
                   fields: List[str] = None,
                   link: str = None,
                   link_fields: List[str] = None,
                   rel_fields: List[str] = None,
                   **kwargs) -> Union[None, NeoQuerySet, NeoLinkedQuerySet, NeoHyperLinkedQuerySet]:
    """
    Filter all objects from the database of a given node type.
    If a link is requested,
    the link/relationship fields will be also retrieved from all objects related with each single object
    """
    query_set = get_query_set(cls=cls, fields=fields, link=link, link_fields=link_fields, rel_fields=rel_fields)
    return query_set.filter(**kwargs)


@raise_exception
def order_by_objects(cls: _model_type, fields: List[str] = None, *args) -> List[DjangoNode]:
    """
    Get and order by fields all objects from database
    """
    if not fields:
        fields = ['protrend_id']

    node_cls = node_factory(fields)

    nodes = []
    for node in cls.nodes.order_by(*args):
        kwargs = {attr: getattr(node, attr, None) for attr in fields}
        new_node = node_cls(**kwargs)
        nodes.append(new_node)

    return nodes


# ---------------------------------------------------------
# Single Object Queries
# ---------------------------------------------------------
@raise_exception
def get_object(cls: _model_type,
               fields: List[str] = None,
               link: str = None,
               link_fields: List[str] = None,
               rel_fields: List[str] = None,
               **kwargs) -> Union[None, _model]:
    """
    Get an object from the database of a given node type.
    If a link is requested,
    the link/relationship fields will be also retrieved from all objects related with each single object
    """
    query_set = get_query_set(cls=cls, fields=fields, link=link, link_fields=link_fields, rel_fields=rel_fields)
    objs = query_set.get(**kwargs)

    if len(objs) == 1:
        return objs[0]
    return


@raise_exception
def get_first_object(cls: _model_type,
                     fields: List[str] = None,
                     link: str = None,
                     link_fields: List[str] = None,
                     rel_fields: List[str] = None) -> Union[None, _model]:
    """
    Get the first object from database
    """
    query_set = get_query_set(cls=cls, fields=fields, link=link, link_fields=link_fields, rel_fields=rel_fields)
    objs = query_set.all()

    if objs:
        return objs[0]

    return


@raise_exception
def get_last_object(cls: _model_type,
                    fields: List[str] = None,
                    link: str = None,
                    link_fields: List[str] = None,
                    rel_fields: List[str] = None) -> Union[None, _model]:
    """
    Get the last object from database
    """
    query_set = get_query_set(cls=cls, fields=fields, link=link, link_fields=link_fields, rel_fields=rel_fields)
    objs = query_set.all()

    if objs:
        return objs[-1]

    return
