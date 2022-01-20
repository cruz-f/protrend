from typing import Union, Type, Any, List, Dict

from django.db.models import Model, QuerySet
from django_neomodel import DjangoNode
from neomodel import NodeSet, MultipleNodesReturned

_model_type = Union[Type[DjangoNode], Type[Model]]
_model = Union[DjangoNode, Model]


def get_query_set(cls: _model_type) -> Union[Any, NodeSet, QuerySet]:
    if hasattr(cls, 'nodes'):
        return cls.nodes

    if hasattr(cls, 'objects'):
        return cls.objects

    raise AttributeError(f'objects or nodes attribute not found for type object {cls.__name__}')


# ---------------------------------------------------------
# Bulk Object Create Read Update and Delete operations
# ---------------------------------------------------------
def get_objects(cls: _model_type) -> Union[List[DjangoNode], List[Model]]:
    """
    Get objects from database
    """
    query_set = get_query_set(cls)
    return list(query_set.all())


def filter_objects(cls: _model_type, *args, **kwargs) -> Union[List[DjangoNode], List[Model]]:
    """
    Get and filter objects from database
    """
    query_set = get_query_set(cls)
    return list(query_set.filter(*args, **kwargs))


def order_by_objects(cls: _model_type, *fields) -> Union[List[DjangoNode], List[Model]]:
    """
    Get and order by fields all objects from database
    """
    query_set = get_query_set(cls)
    return list(query_set.order_by(*fields))


def create_objects(cls: _model_type, *objects: Dict[str, Any]) -> Union[List[DjangoNode], List[Model]]:
    """
    Create multiple objects into the database from a set of dictionaries
    """
    if hasattr(cls, 'create'):
        return cls.create(*objects)

    if hasattr(cls, 'objects'):
        return [cls(**kwargs).save() for kwargs in objects]

    return []


def delete_objects(*objects: _model):
    """
    Delete multiple objects from the database calling the delete method of these objects
    """
    for obj in objects:
        obj.delete()


# ---------------------------------------------------------
# Single Object Create Read Update and Delete operations
# ---------------------------------------------------------
def get_object(cls: _model_type, **kwargs) -> Union[_model, None]:
    """
    Get an object from database according to the parameters
    """
    query_set = get_query_set(cls)

    try:
        return query_set.get(**kwargs)

    except cls.DoesNotExist:
        return

    except MultipleNodesReturned:
        return

    except cls.MultipleObjectsReturned:
        return


def create_object(cls: _model_type, **kwargs) -> _model:
    """
    Create an object into the database according to the parameters
    """
    obj = cls(**kwargs)
    obj.save()
    return obj


def update_object(obj: _model, **kwargs) -> _model:
    """
    Update an object into the database according to the parameters
    """
    for attr, value in kwargs.items():
        setattr(obj, attr, value)
    obj.save()
    return obj


def delete_object(obj: _model):
    """
    Delete an object from the database
    """
    obj.delete()
