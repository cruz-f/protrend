from typing import List, Dict, Any

from rest_framework import status

from data import TFBS
import domain.model_api as mapi
from domain.database._validate import _validate_args_by_site_hash, _validate_kwargs_by_site_hash
from domain.database.organism import get_organism_by_id
from exceptions import ProtrendException


_HEADER = 'PRT'
_ENTITY = 'TBS'


def create_biding_sites(*biding_sites: Dict[str, Any]) -> List[TFBS]:
    """
    Create biding_sites into the database
    """
    for site in biding_sites:
        organism = site['organism']
        obj = get_organism_by_id(organism)
        if obj is None:
            raise ProtrendException(detail=f'The submitted {organism} protrend id for the property organism '
                                           f'was not found in the database.',
                                    code='create or update error',
                                    status=status.HTTP_400_BAD_REQUEST)

    biding_sites = _validate_args_by_site_hash(args=biding_sites, node_cls=TFBS, header=_HEADER, entity=_ENTITY)
    return mapi.create_objects(TFBS, *biding_sites)


def delete_biding_sites(*biding_sites: TFBS):
    """
    Delete biding_sites from the database
    """
    return mapi.delete_objects(*biding_sites)


def create_biding_site(**kwargs) -> TFBS:
    """
    Create a given biding_site into the database according to the parameters
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


def update_biding_site(biding_site: TFBS, **kwargs) -> TFBS:
    """
    Update the biding_site into the database according to the parameters
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
    return mapi.update_object(biding_site, **kwargs)


def delete_biding_site(biding_site: TFBS) -> TFBS:
    """
    Delete the biding_site from the database
    """
    return mapi.delete_object(biding_site)
