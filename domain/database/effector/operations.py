from typing import List, Dict, Any

import domain.model_api as mapi
from data import Effector
from exceptions import ProtrendException
from transformers import lstrip, rstrip, lower, apply_transformers
from ..utils import protrend_id_decoder, protrend_id_encoder, protrend_identifiers_batch


def create_effectors(*effectors: Dict[str, Any]) -> List[Effector]:
    """
    Create effectors into the database
    """
    names = []
    for effector in effectors:
        name = apply_transformers(str(effector['name']), lower, rstrip, lstrip)
        names.append(name)

    current_objs = mapi.order_by_objects(Effector, 'protrend_id')
    for obj in current_objs:
        obj_name = apply_transformers(obj.name, lower, rstrip, lstrip)
        if obj_name in names:
            raise ProtrendException(detail=f'Object with name {obj_name} already exists in the database and '
                                    f'has the following protrend_id: {obj.protrend_id}',
                                    code='create error')

    if current_objs:
        last_obj = current_objs[-1]
        idx = protrend_id_decoder(last_obj.protrend_id) + 1

    else:
        idx = 1

    size = len(effectors)
    new_ids = protrend_identifiers_batch(header='PRT', entity='EFC', start=idx, size=size)

    for effector, new_id in zip(effectors, new_ids):
        effector['protrend_id'] = new_id

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
    submitted_name = str(kwargs['name'])
    name = apply_transformers(submitted_name, lower, rstrip, lstrip)

    current_objs = mapi.order_by_objects(Effector, 'protrend_id')
    for obj in current_objs:
        obj_name = apply_transformers(obj.name, lower, rstrip, lstrip)
        if name == obj_name:
            raise ProtrendException(detail=f'Object with name {obj_name} already exists in the database and '
                                           f'has the following protrend_id: {obj.protrend_id}',
                                    code='create error')

    if current_objs:
        last_obj = current_objs[-1]
        idx = protrend_id_decoder(last_obj.protrend_id) + 1

    else:
        idx = 1

    new_id = protrend_id_encoder(header='PRT', entity='EFC', integer=idx)
    kwargs['protrend_id'] = new_id
    return mapi.create_object(Effector, **kwargs)


def update_effector(effector: Effector, **kwargs) -> Effector:
    """
    Update the effector into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='update error')
    return mapi.update_object(effector, **kwargs)


def delete_effector(effector: Effector) -> Effector:
    """
    Delete the effector from the database
    """
    return mapi.delete_object(effector)
