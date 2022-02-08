from functools import wraps
from typing import Union, Type, Any, List, Dict, Callable, Tuple

from django.db.models import Model, QuerySet
from django_neomodel import DjangoNode
from neo4j.exceptions import DriverError, Neo4jError
from neomodel import NodeSet, MultipleNodesReturned, StructuredRel, RelationshipManager, NeomodelException
from rest_framework import status

from exceptions import ProtrendException
from set_list import SetList

_model_type = Union[Type[DjangoNode], Type[Model]]
_model = Union[DjangoNode, Model]


def get_query_set(cls: _model_type) -> Union[Any, NodeSet, QuerySet]:
    if hasattr(cls, 'nodes'):
        return cls.nodes

    if hasattr(cls, 'objects'):
        return cls.objects

    raise AttributeError(f'objects or nodes attribute not found for type object {cls.__name__}')


def run_or_raise(fn: Callable):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)

        except (AttributeError, NeomodelException, Neo4jError, DriverError):
            raise ProtrendException(detail='ProTReND database is currently unavailable. '
                                           'Please try again later or contact the support team',
                                    code='service unavailable',
                                    status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return wrapper


# ---------------------------------------------------------
# Bulk Object Create Read Update and Delete operations
# ---------------------------------------------------------
@run_or_raise
def get_objects(cls: _model_type) -> Union[List[DjangoNode], List[Model]]:
    """
    Get objects from database
    """
    query_set = get_query_set(cls)
    return list(query_set.all())


@run_or_raise
def filter_objects(cls: _model_type, *args, **kwargs) -> Union[List[DjangoNode], List[Model]]:
    """
    Get and filter objects from database
    """
    query_set = get_query_set(cls)
    return list(query_set.filter(*args, **kwargs))


@run_or_raise
def order_by_objects(cls: _model_type, *fields) -> Union[List[DjangoNode], List[Model]]:
    """
    Get and order by fields all objects from database
    """
    query_set = get_query_set(cls)
    return list(query_set.order_by(*fields))


@run_or_raise
def create_objects(cls: _model_type, *objects: Dict[str, Any]) -> Union[List[DjangoNode], List[Model]]:
    """
    Create multiple objects into the database from a set of dictionaries
    """
    if hasattr(cls, 'create'):
        return cls.create(*objects)

    if hasattr(cls, 'objects'):
        return [cls(**kwargs).save() for kwargs in objects]

    return []


@run_or_raise
def delete_objects(*objects: _model):
    """
    Delete multiple objects from the database calling the delete method of these objects
    """
    for obj in objects:
        obj.delete()


# ---------------------------------------------------------
# Single Object Create Read Update and Delete operations
# ---------------------------------------------------------
@run_or_raise
def get_object(cls: _model_type, **kwargs) -> Union[_model, None]:
    """
    Get an object from database according to the parameters
    """
    query_set = get_query_set(cls)

    try:
        return query_set.get_or_none(**kwargs)

    except MultipleNodesReturned:
        return


@run_or_raise
def get_first_object(cls: _model_type, *fields) -> Union[_model, None]:
    """
    Get the first object from database according to the fields
    """
    objs = order_by_objects(cls, *fields)
    if objs:
        return objs[0]

    return


@run_or_raise
def get_last_object(cls: _model_type, *fields) -> Union[_model, None]:
    """
    Get the last object from database according to the fields
    """
    objs = order_by_objects(cls, *fields)
    if objs:
        return objs[-1]

    return


@run_or_raise
def create_object(cls: _model_type, **kwargs) -> _model:
    """
    Create an object into the database according to the parameters
    """
    obj = cls(**kwargs)
    obj.save()
    return obj


@run_or_raise
def update_object(obj: _model, **kwargs) -> _model:
    """
    Update an object into the database according to the parameters
    """
    for attr, value in kwargs.items():
        setattr(obj, attr, value)
    obj.save()
    return obj


@run_or_raise
def delete_object(obj: _model):
    """
    Delete an object from the database
    """
    obj.delete()


# ------------------------------------------------------------------------------
# Relationships - SO FAR THE DOMAIN LAYER ONLY SUPPORTS NEOMODEL RELATIONSHIPS
# ------------------------------------------------------------------------------
def get_rel_query_set(obj: _model, rel: str) -> Union[Any, RelationshipManager]:
    relationship = getattr(obj, rel, None)
    if relationship is not None:
        if hasattr(relationship, 'all'):
            return relationship

    raise AttributeError(f'relationship attribute not found for object {obj.protrend_id}')


# ---------------------------------------------------------
# Relationships Create Read Update and Delete operations
# ---------------------------------------------------------
@run_or_raise
def get_related_objects(obj: _model, rel: str) -> SetList[DjangoNode]:
    """
    Get all objects connected with this object
    """
    query_set = get_rel_query_set(obj=obj, rel=rel)
    return SetList(query_set.all())


@run_or_raise
def filter_related_objects(obj: _model, rel: str, **kwargs) -> SetList[DjangoNode]:
    """
    Get and filter the objects connected with this object
    """
    query_set = get_rel_query_set(obj=obj, rel=rel)
    return SetList(query_set.filter(**kwargs))


@run_or_raise
def order_by_related_objects(obj: _model, rel: str, *fields) -> SetList[DjangoNode]:
    """
    Get and order by fields the objects connected with this object
    """
    query_set = get_rel_query_set(obj=obj, rel=rel)
    return SetList(query_set.order_by(*fields))


@run_or_raise
def get_related_object(obj: _model, rel: str, **kwargs) -> Union[DjangoNode, None]:
    """
    Get a specific object (by identifier, etc) connected with this object
    """
    query_set = get_rel_query_set(obj=obj, rel=rel)

    try:
        return query_set.get_or_none(**kwargs)

    except MultipleNodesReturned:

        nodes = SetList(query_set.all())
        for node in nodes:

            matches = [getattr(node, key) == value
                       for key, value in kwargs.items()]

            if all(matches):
                return node

    return


@run_or_raise
def get_relationships(source: _model, rel: str, target: _model) -> List[StructuredRel]:
    """
    Get all relationships objects between two objects
    """
    query_set = get_rel_query_set(obj=source, rel=rel)
    return list(query_set.all_relationships(target))


@run_or_raise
def delete_relationships(source: _model, rel: str, target: _model):
    """
    Delete all relationships between two objects
    """
    query_set = get_rel_query_set(obj=source, rel=rel)
    return query_set.disconnect(target)


@run_or_raise
def get_relationship(source: _model, rel: str, target: _model) -> Union[StructuredRel, None]:
    """
    Get the first relationship object between two nodes
    """
    query_set = get_rel_query_set(obj=source, rel=rel)
    return query_set.relationship(target)


@run_or_raise
def is_connected(source: _model, rel: str, target: _model) -> Union[StructuredRel, None]:
    """
    Get the first relationship object between two nodes
    """
    query_set = get_rel_query_set(obj=source, rel=rel)
    return query_set.is_connected(target)


@run_or_raise
def create_relationship(source: _model, rel: str, target: _model, **kwargs) -> Union[StructuredRel, None]:
    """
    Create a relationship object between two objects
    """
    query_set = get_rel_query_set(obj=source, rel=rel)
    return query_set.connect(target, properties=kwargs)


@run_or_raise
def create_unique_relationship(source: _model,
                               rel: str,
                               target: _model,
                               **kwargs) -> Union[StructuredRel, None]:
    """
    Create a relationship object between two objects
    """
    query_set = get_rel_query_set(obj=source, rel=rel)

    if not query_set.is_connected(target):
        return query_set.connect(target, properties=kwargs)

    return


@run_or_raise
def create_unique_reverse_relationship(source: _model,
                                       forward_rel: str,
                                       backward_rel: str,
                                       target: _model,
                                       **kwargs) -> Tuple[Union[StructuredRel, None], Union[StructuredRel, None]]:
    """
    Create a forward and backward relationship object between two objects if these are not connected
    """
    forward_instance = None
    backward_instance = None

    forward_query_set = get_rel_query_set(obj=source, rel=forward_rel)
    if not forward_query_set.is_connected(target):
        forward_instance = forward_query_set.connect(target, properties=kwargs)

    backward_query_set = get_rel_query_set(obj=target, rel=backward_rel)
    if not backward_query_set.is_connected(source):
        backward_instance = backward_query_set.connect(source, properties=kwargs)

    return forward_instance, backward_instance


@run_or_raise
def update_relationship(source: _model, rel: str, target: _model, **kwargs) -> StructuredRel:
    """
    Update a relationship object between two objects
    """
    relationship = get_relationship(source=source, rel=rel, target=target)
    for attr, value in kwargs.items():
        setattr(relationship, attr, value)
    relationship.save()
    return relationship


@run_or_raise
def delete_relationship(source: _model, rel: str, target: _model):
    """
    Delete a relationship object between two objects
    """
    return delete_relationships(source=source, rel=rel, target=target)
