from typing import List

from data import Effector
import domain.model_api as mapi


def get_effectors() -> List[Effector]:
    """
    Get effectors list from database
    """
    return mapi.get_objects(Effector)


def filter_effectors(*args, **kwargs) -> List[Effector]:
    """
    Get and filter effectors from database
    """
    return mapi.filter_objects(Effector, *args, **kwargs)


def order_by_effectors(*fields) -> List[Effector]:
    """
    Get and order by effectors from database
    """
    return mapi.order_by_objects(Effector, *fields)


def order_effectors_by_id() -> List[Effector]:
    """
    Get and order by effectors by protrend identifier from database
    """
    return mapi.order_by_objects(Effector, 'protrend_id')


def get_effector(**kwargs) -> Effector:
    """
    Get a given effector from database
    """
    return mapi.get_object(Effector, **kwargs)


def get_effector_by_id(protrend_id: str) -> Effector:
    """
    Get a given effector from database using the protrend identifier
    """
    return mapi.get_object(Effector, protrend_id=protrend_id)


def get_last_effector() -> Effector:
    """
    Get the last effector from database using the protrend identifier
    """
    return mapi.get_last_object(Effector, 'protrend_id')
