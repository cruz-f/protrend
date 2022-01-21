from typing import List, Dict, Any

from rest_framework import status

import domain.model_api as mapi
from data import Effector
from exceptions import ProtrendException
from .._validate import _validate_kwargs_by_name, _validate_args_by_name


_HEADER = 'PRT'
_ENTITY = 'EFC'


def create_effectors(*effectors: Dict[str, Any]) -> List[Effector]:
    """
    Create effectors into the database
    """
    effectors = _validate_args_by_name(args=effectors, node_cls=Effector, header=_HEADER, entity=_ENTITY)
    return mapi.create_objects(Effector, *effectors)


def delete_effectors(*effectors: Effector):
    """
    Delete effectors from the database
    """
    return mapi.delete_objects(*effectors)


def create_effector(**kwargs) -> Effector:
    """
    Create a given effector into the database according to the parameters
    """
    kwargs = _validate_kwargs_by_name(kwargs=kwargs, node_cls=Effector, header=_HEADER, entity=_ENTITY)
    return mapi.create_object(Effector, **kwargs)


def update_effector(effector: Effector, **kwargs) -> Effector:
    """
    Update the effector into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    if 'name' not in kwargs:
        return mapi.update_object(effector, **kwargs)

    _ = _validate_kwargs_by_name(kwargs=kwargs, node_cls=Effector, header=_HEADER, entity=_ENTITY)
    return mapi.update_object(effector, **kwargs)


def delete_effector(effector: Effector) -> Effector:
    """
    Delete the effector from the database
    """
    return mapi.delete_object(effector)
