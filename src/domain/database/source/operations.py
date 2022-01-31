from typing import List, Dict, Any

from rest_framework import status

from data import Source
import domain.model_api as mapi
from domain.database._validate import _validate_kwargs_by_name, _validate_args_by_name
from exceptions import ProtrendException


_HEADER = 'PRT'
_ENTITY = 'SRC'


def create_sources(*sources: Dict[str, Any]) -> List[Source]:
    """
    Create sources into the database
    """
    sources = _validate_args_by_name(args=sources, node_cls=Source, header=_HEADER, entity=_ENTITY)
    return mapi.create_objects(Source, *sources)


def delete_sources(*sources: Source):
    """
    Delete sources from the database
    """
    return mapi.delete_objects(*sources)


def create_source(**kwargs) -> Source:
    """
    Create a given source into the database according to the parameters
    """
    kwargs = _validate_kwargs_by_name(kwargs=kwargs, node_cls=Source, header=_HEADER, entity=_ENTITY)
    return mapi.create_object(Source, **kwargs)


def update_source(source: Source, **kwargs) -> Source:
    """
    Update the source into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    if 'name' in kwargs:
        name = kwargs['name']
        if name != source.name:
            kwargs = _validate_kwargs_by_name(kwargs=kwargs, node_cls=Source, header=_HEADER, entity=_ENTITY)
            kwargs.pop('protrend_id')

    return mapi.update_object(source, **kwargs)


def delete_source(source: Source) -> Source:
    """
    Delete the source from the database
    """
    return mapi.delete_object(source)
