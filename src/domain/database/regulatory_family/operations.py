from typing import List, Dict, Any

from rest_framework import status

from data import RegulatoryFamily
import domain.model_api as mapi
from domain.database._validate import _validate_kwargs_by_name, _validate_args_by_name
from exceptions import ProtrendException


_HEADER = 'PRT'
_ENTITY = 'RFAM'


def create_rfams(*rfams: Dict[str, Any]) -> List[RegulatoryFamily]:
    """
    Create rfams into the database
    """
    rfams = _validate_args_by_name(args=rfams, node_cls=RegulatoryFamily, header=_HEADER, entity=_ENTITY)
    return mapi.create_objects(RegulatoryFamily, *rfams)


def delete_rfams(*rfams: RegulatoryFamily):
    """
    Delete rfams from the database
    """
    return mapi.delete_objects(*rfams)


def create_rfam(**kwargs) -> RegulatoryFamily:
    """
    Create a given rfam into the database according to the parameters
    """
    kwargs = _validate_kwargs_by_name(kwargs=kwargs, node_cls=RegulatoryFamily, header=_HEADER, entity=_ENTITY)
    return mapi.create_object(RegulatoryFamily, **kwargs)


def update_rfam(rfam: RegulatoryFamily, **kwargs) -> RegulatoryFamily:
    """
    Update the rfam into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    if 'name' in kwargs:
        name = kwargs['name']
        if name != rfam.name:
            kwargs = _validate_kwargs_by_name(kwargs=kwargs, node_cls=RegulatoryFamily, header=_HEADER, entity=_ENTITY)
            kwargs.pop('protrend_id')

    return mapi.update_object(rfam, **kwargs)


def delete_rfam(rfam: RegulatoryFamily) -> RegulatoryFamily:
    """
    Delete the rfam from the database
    """
    return mapi.delete_object(rfam)
