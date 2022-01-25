from typing import List, Dict, Any

from rest_framework import status

from data import TFBS
import domain.model_api as mapi
from domain.database._validate import _validate_args_by_site_hash, _validate_kwargs_by_site_hash
from domain.database.organism import get_organism_by_id
from exceptions import ProtrendException


_HEADER = 'PRT'
_ENTITY = 'TBS'


def create_binding_sites(*binding_sites: Dict[str, Any]) -> List[TFBS]:
    """
    Create binding_sites into the database
    """
    for site in binding_sites:
        organism = site['organism']
        obj = get_organism_by_id(organism)
        if obj is None:
            raise ProtrendException(detail=f'The submitted {organism} protrend id for the property organism '
                                           f'was not found in the database.',
                                    code='create or update error',
                                    status=status.HTTP_400_BAD_REQUEST)

    binding_sites = _validate_args_by_site_hash(args=binding_sites, node_cls=TFBS, header=_HEADER, entity=_ENTITY)
    return mapi.create_objects(TFBS, *binding_sites)


def delete_binding_sites(*binding_sites: TFBS):
    """
    Delete binding_sites from the database
    """
    return mapi.delete_objects(*binding_sites)


def create_binding_site(**kwargs) -> TFBS:
    """
    Create a given binding_site into the database according to the parameters
    """
    organism = kwargs['organism']
    obj = get_organism_by_id(organism)
    if obj is None:
        raise ProtrendException(detail=f'The submitted {organism} protrend id for the property organism '
                                       f'was not found in the database.',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    kwargs = _validate_kwargs_by_site_hash(kwargs=kwargs, node_cls=TFBS, header=_HEADER, entity=_ENTITY)
    return mapi.create_object(TFBS, **kwargs)


def update_binding_site(binding_site: TFBS, **kwargs) -> TFBS:
    """
    Update the binding_site into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    if 'organism' in kwargs:
        organism = kwargs['organism']
        obj = get_organism_by_id(organism)
        if obj is None:
            raise ProtrendException(detail=f'The submitted {organism} protrend id for the property organism '
                                           f'was not found in the database.',
                                    code='create or update error',
                                    status=status.HTTP_400_BAD_REQUEST)

    # the protrend hash must always be regenerated
    kwargs = _validate_kwargs_by_site_hash(kwargs=kwargs, node_cls=TFBS, header=_HEADER, entity=_ENTITY)
    return mapi.update_object(binding_site, **kwargs)


def delete_binding_site(binding_site: TFBS) -> TFBS:
    """
    Delete the binding_site from the database
    """
    return mapi.delete_object(binding_site)
