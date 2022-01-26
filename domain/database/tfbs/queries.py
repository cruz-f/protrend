from typing import List

from data import TFBS
import domain.model_api as mapi


def get_binding_sites() -> List[TFBS]:
    """
    Get binding_sites list from database
    """
    return mapi.get_objects(TFBS)


def filter_binding_sites(*args, **kwargs) -> List[TFBS]:
    """
    Get and filter binding_sites from database
    """
    return mapi.filter_objects(TFBS, *args, **kwargs)


def order_by_binding_sites(*fields) -> List[TFBS]:
    """
    Get and order by binding_sites from database
    """
    return mapi.order_by_objects(TFBS, *fields)


def order_binding_sites_by_id() -> List[TFBS]:
    """
    Get and order by binding_sites by protrend identifier from database
    """
    return mapi.order_by_objects(TFBS, 'protrend_id')


def get_binding_site(**kwargs) -> TFBS:
    """
    Get a given binding_site from database
    """
    return mapi.get_object(TFBS, **kwargs)


def get_binding_site_by_id(protrend_id: str) -> TFBS:
    """
    Get a given binding_site from database using the protrend identifier
    """
    return mapi.get_object(TFBS, protrend_id=protrend_id)


def get_last_binding_site() -> TFBS:
    """
    Get the last binding_site from database using the protrend identifier
    """
    return mapi.get_last_object(TFBS, 'protrend_id')
