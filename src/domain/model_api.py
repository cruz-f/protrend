from functools import wraps
from typing import Union, Type, Any, List, Dict, Callable

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
def get_rel_query_set(obj: _model, target: str) -> Union[Any, RelationshipManager]:
    relationship = getattr(obj, target, None)
    if relationship is not None:
        if hasattr(relationship, 'all'):
            return relationship

    raise AttributeError(f'relationship attribute not found for object {obj.protrend_id}')


# ---------------------------------------------------------
# Relationships Create Read Update and Delete operations
# ---------------------------------------------------------
@run_or_raise
def get_related_objects(obj: _model, target: str) -> SetList[DjangoNode]:
    """
    Get all objects connected with this object
    """
    query_set = get_rel_query_set(obj=obj, target=target)
    return SetList(query_set.all())


@run_or_raise
def filter_related_objects(obj: _model, target: str, **kwargs) -> SetList[DjangoNode]:
    """
    Get and filter the objects connected with this object
    """
    query_set = get_rel_query_set(obj=obj, target=target)
    return SetList(query_set.filter(**kwargs))


@run_or_raise
def order_by_related_objects(obj: _model, target: str, *fields) -> SetList[DjangoNode]:
    """
    Get and order by fields the objects connected with this object
    """
    query_set = get_rel_query_set(obj=obj, target=target)
    return SetList(query_set.order_by(*fields))


@run_or_raise
def get_related_object(obj: _model, target: str, **kwargs) -> Union[DjangoNode, None]:
    """
    Get a specific object (by identifier, etc) connected with this object
    """
    query_set = get_rel_query_set(obj=obj, target=target)

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
def get_relationships(source_obj: _model, target: str, target_obj: _model) -> List[StructuredRel]:
    """
    Get all relationships objects between two objects
    """
    query_set = get_rel_query_set(obj=source_obj, target=target)
    return list(query_set.all_relationships(target_obj))


@run_or_raise
def delete_relationships(source_obj: _model, target: str, target_obj: _model):
    """
    Delete all relationships between two objects
    """
    query_set = get_rel_query_set(obj=source_obj, target=target)
    return query_set.disconnect(target_obj)


@run_or_raise
def get_relationship(source_obj: _model, target: str, target_obj: _model) -> Union[StructuredRel, None]:
    """
    Get the first relationship object between two nodes
    """
    query_set = get_rel_query_set(obj=source_obj, target=target)
    return query_set.relationship(target_obj)


@run_or_raise
def is_connected(source_obj: _model, target: str, target_obj: _model) -> Union[StructuredRel, None]:
    """
    Get the first relationship object between two nodes
    """
    query_set = get_rel_query_set(obj=source_obj, target=target)
    return query_set.is_connected(target_obj)


@run_or_raise
def create_relationship(source_obj: _model, target: str, target_obj: _model, **kwargs) -> Union[StructuredRel, None]:
    """
    Create a relationship object between two objects
    """
    query_set = get_rel_query_set(obj=source_obj, target=target)
    return query_set.connect(target_obj, properties=kwargs)


@run_or_raise
def create_or_none(source_obj: _model, target: str, target_obj: _model, **kwargs) -> Union[StructuredRel, None]:
    """
    Create a relationship object between two objects
    """
    query_set = get_rel_query_set(obj=source_obj, target=target)

    if not query_set.is_connected(target_obj):
        return query_set.connect(target_obj, properties=kwargs)

    return


@run_or_raise
def update_relationship(source_obj: _model, target: str, target_obj: _model, **kwargs) -> StructuredRel:
    """
    Update a relationship object between two objects
    """
    relationship = get_relationship(source_obj=source_obj, target=target, target_obj=target_obj)
    for attr, value in kwargs.items():
        setattr(relationship, attr, value)
    relationship.save()
    return relationship


@run_or_raise
def delete_relationship(source_obj: _model, target: str, target_obj: _model):
    """
    Delete a relationship object between two objects
    """
    return delete_relationships(source_obj=source_obj, target=target, target_obj=target_obj)
