from typing import List, Dict, Any

from rest_framework import status

from data import Pathway
import domain.model_api as mapi
from domain.database._validate import _validate_args_by_name, _validate_kwargs_by_name
from exceptions import ProtrendException


_HEADER = 'PRT'
_ENTITY = 'PTH'


def create_pathways(*pathways: Dict[str, Any]) -> List[Pathway]:
    """
    Create pathways into the database
    """
    pathways = _validate_args_by_name(args=pathways, node_cls=Pathway, header=_HEADER, entity=_ENTITY)
    return mapi.create_objects(Pathway, *pathways)


def delete_pathways(*pathways: Pathway):
    """
    Delete pathways from the database
    """
    return mapi.delete_objects(*pathways)


def create_pathway(**kwargs) -> Pathway:
    """
    Create a given pathway into the database according to the parameters
    """
    kwargs = _validate_kwargs_by_name(kwargs=kwargs, node_cls=Pathway, header=_HEADER, entity=_ENTITY)
    return mapi.create_object(Pathway, **kwargs)


def update_pathway(pathway: Pathway, **kwargs) -> Pathway:
    """
    Update the pathway into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    if 'name' in kwargs:
        _validate_kwargs_by_name(kwargs=kwargs, node_cls=Pathway, header=_HEADER, entity=_ENTITY)

    return mapi.update_object(pathway, **kwargs)


def delete_pathway(pathway: Pathway) -> Pathway:
    """
    Delete the pathway from the database
    """
    return mapi.delete_object(pathway)
