from typing import List

from data import TFBS
import domain.model_api as mapi


def get_biding_sites() -> List[TFBS]:
    """
    Get biding_sites list from database
    """
    return mapi.get_objects(TFBS)


def filter_biding_sites(*args, **kwargs) -> List[TFBS]:
    """
    Get and filter biding_sites from database
    """
    return mapi.filter_objects(TFBS, *args, **kwargs)


def order_by_biding_sites(*fields) -> List[TFBS]:
    """
    Get and order by biding_sites from database
    """
    return mapi.order_by_objects(TFBS, *fields)


def order_biding_sites_by_id() -> List[TFBS]:
    """
    Get and order by biding_sites by protrend identifier from database
    """
    return mapi.order_by_objects(TFBS, 'protrend_id')


def get_biding_site(**kwargs) -> TFBS:
    """
    Get a given biding_site from database
    """
    return mapi.get_object(TFBS, **kwargs)


def get_biding_site_by_id(protrend_id: str) -> TFBS:
    """
    Get a given biding_site from database using the protrend identifier
    """
    return mapi.get_object(TFBS, protrend_id=protrend_id)


def get_last_biding_site() -> TFBS:
    """
    Get the last biding_site from database using the protrend identifier
    """
    return mapi.get_last_object(TFBS, 'protrend_id')
