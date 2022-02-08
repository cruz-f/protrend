from typing import List, Dict, Any

from rest_framework import status

from data import Evidence
import domain.model_api as mapi
from domain.database._validate import _validate_args_by_name, _validate_kwargs_by_name
from exceptions import ProtrendException


_HEADER = 'PRT'
_ENTITY = 'EVI'


def create_evidences(*evidences: Dict[str, Any]) -> List[Evidence]:
    """
    Create evidences into the database
    """
    evidences = _validate_args_by_name(args=evidences, node_cls=Evidence, header=_HEADER, entity=_ENTITY)
    return mapi.create_objects(Evidence, *evidences)


def delete_evidences(*evidences: Evidence):
    """
    Delete evidences from the database
    """
    return mapi.delete_objects(*evidences)


def create_evidence(**kwargs) -> Evidence:
    """
    Create a given evidence into the database according to the parameters
    """
    kwargs = _validate_kwargs_by_name(kwargs=kwargs, node_cls=Evidence, header=_HEADER, entity=_ENTITY)
    return mapi.create_object(Evidence, **kwargs)


def update_evidence(evidence: Evidence, **kwargs) -> Evidence:
    """
    Update the evidence into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    if 'name' in kwargs:
        name = kwargs['name']
        if name != evidence.name:
            kwargs = _validate_kwargs_by_name(kwargs=kwargs, node_cls=Evidence, header=_HEADER, entity=_ENTITY)
            kwargs.pop('protrend_id')

    return mapi.update_object(evidence, **kwargs)


def delete_evidence(evidence: Evidence) -> Evidence:
    """
    Delete the evidence from the database
    """
    return mapi.delete_object(evidence)
