from typing import List

from data import RegulatoryFamily
import domain.model_api as mapi


def get_rfams() -> List[RegulatoryFamily]:
    """
    Get rfams list from database
    """
    return mapi.get_objects(RegulatoryFamily)


def filter_rfams(*args, **kwargs) -> List[RegulatoryFamily]:
    """
    Get and filter rfams from database
    """
    return mapi.filter_objects(RegulatoryFamily, *args, **kwargs)


def order_by_rfams(*fields) -> List[RegulatoryFamily]:
    """
    Get and order by rfams from database
    """
    return mapi.order_by_objects(RegulatoryFamily, *fields)


def order_rfams_by_id() -> List[RegulatoryFamily]:
    """
    Get and order by rfams by protrend identifier from database
    """
    return mapi.order_by_objects(RegulatoryFamily, 'protrend_id')


def get_rfam(**kwargs) -> RegulatoryFamily:
    """
    Get a given rfam from database
    """
    return mapi.get_object(RegulatoryFamily, **kwargs)


def get_rfam_by_id(protrend_id: str) -> RegulatoryFamily:
    """
    Get a given rfam from database using the protrend identifier
    """
    return mapi.get_object(RegulatoryFamily, protrend_id=protrend_id)


def get_last_rfam() -> RegulatoryFamily:
    """
    Get the last rfam from database using the protrend identifier
    """
    return mapi.get_last_object(RegulatoryFamily, 'protrend_id')
