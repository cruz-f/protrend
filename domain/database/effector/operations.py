from typing import List, Dict, Any

from rest_framework import status

import domain.model_api as mapi
from data import Effector
from exceptions import ProtrendException
from transformers import lstrip, rstrip, lower, to_str
from .._sanity import _sanitize_duplicates, _sanitize_protrend_idx, _sanitize_factor
from ..utils import protrend_id_encoder


def create_effectors(*effectors: Dict[str, Any]) -> List[Effector]:
    """
    Create effectors into the database
    """
    for effector in effectors:
        obj = _sanitize_duplicates(value=effector['name'],
                                   transformers=[to_str, lower, rstrip, lstrip],
                                   node_cls=Effector,
                                   key='name_factor')

        if obj is not None:
            raise ProtrendException(detail=f'Object with name {obj.name} already exists in the database and '
                                           f'has the following protrend_id: {obj.protrend_id}',
                                    code='create error',
                                    status=status.HTTP_400_BAD_REQUEST)
    idx = _sanitize_protrend_idx(Effector)

    for i, effector in enumerate(effectors):
        i = i + idx + 1
        new_id = protrend_id_encoder(header='PRT', entity='RFC', integer=i)
        effector['protrend_id'] = new_id

        new_factor = _sanitize_factor(value=effector['name'], transformers=[to_str, lower, rstrip, lstrip])
        effector['name_factor'] = new_factor

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
    obj = _sanitize_duplicates(value=kwargs['name'],
                               transformers=[to_str, lower, rstrip, lstrip],
                               node_cls=Effector,
                               key='name_factor')

    if obj is not None:
        raise ProtrendException(detail=f'Object with name {obj.name} already exists in the database and '
                                       f'has the following protrend_id: {obj.protrend_id}',
                                code='create error',
                                status=status.HTTP_400_BAD_REQUEST)

    idx = _sanitize_protrend_idx(Effector)
    new_id = protrend_id_encoder(header='PRT', entity='EFC', integer=idx)
    kwargs['protrend_id'] = new_id

    new_factor = _sanitize_factor(value=kwargs['name'], transformers=[to_str, lower, rstrip, lstrip])
    kwargs['name_factor'] = new_factor

    return mapi.create_object(Effector, **kwargs)


def update_effector(effector: Effector, **kwargs) -> Effector:
    """
    Update the effector into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='update error',
                                status=status.HTTP_400_BAD_REQUEST)

    if 'name' not in kwargs:
        return mapi.update_object(effector, **kwargs)

    obj = _sanitize_duplicates(value=kwargs['name'],
                               transformers=[to_str, lower, rstrip, lstrip],
                               node_cls=Effector,
                               key='name_factor')

    if obj is not None:
        raise ProtrendException(detail=f'Object with name {obj.name} already exists in the database and '
                                       f'has the following protrend_id: {obj.protrend_id}. Please create a new one',
                                code='update error',
                                status=status.HTTP_400_BAD_REQUEST)

    return mapi.update_object(effector, **kwargs)


def delete_effector(effector: Effector) -> Effector:
    """
    Delete the effector from the database
    """
    return mapi.delete_object(effector)
