from typing import List, Dict, Any

from rest_framework import status

from data import Operon
import domain.model_api as mapi
from domain.database._validate import _validate_args_by_operon_db_id, _validate_kwargs_by_operon_db_id
from exceptions import ProtrendException

_HEADER = 'PRT'
_ENTITY = 'OPN'


def create_operons(*operons: Dict[str, Any]) -> List[Operon]:
    """
    Create operons into the database
    """
    operons = _validate_args_by_operon_db_id(args=operons, node_cls=Operon, header=_HEADER, entity=_ENTITY)
    return mapi.create_objects(Operon, *operons)


def delete_operons(*operons: Operon):
    """
    Delete operons from the database
    """
    return mapi.delete_objects(*operons)


def create_operon(**kwargs) -> Operon:
    """
    Create a given operon into the database according to the parameters
    """
    kwargs = _validate_kwargs_by_operon_db_id(kwargs=kwargs, node_cls=Operon, header=_HEADER, entity=_ENTITY)
    return mapi.create_object(Operon, **kwargs)


def update_operon(operon: Operon, **kwargs) -> Operon:
    """
    Update the operon into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    if 'operon_db_id' in kwargs:
        operon_db_id = kwargs['operon_db_id']
        if operon_db_id != operon.operon_db_id:
            kwargs = _validate_kwargs_by_operon_db_id(kwargs=kwargs, node_cls=Operon, header=_HEADER, entity=_ENTITY)
            kwargs.pop('protrend_id')

    return mapi.update_object(operon, **kwargs)


def delete_operon(operon: Operon) -> Operon:
    """
    Delete the operon from the database
    """
    return mapi.delete_object(operon)
