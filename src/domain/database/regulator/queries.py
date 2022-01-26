from typing import List

from data import Regulator
import domain.model_api as mapi


def get_regulators() -> List[Regulator]:
    """
    Get regulators list from database
    """
    return mapi.get_objects(Regulator)


def filter_regulators(*args, **kwargs) -> List[Regulator]:
    """
    Get and filter regulators from database
    """
    return mapi.filter_objects(Regulator, *args, **kwargs)


def order_by_regulators(*fields) -> List[Regulator]:
    """
    Get and order by regulators from database
    """
    return mapi.order_by_objects(Regulator, *fields)


def order_regulators_by_id() -> List[Regulator]:
    """
    Get and order by regulators by protrend identifier from database
    """
    return mapi.order_by_objects(Regulator, 'protrend_id')


def get_regulator(**kwargs) -> Regulator:
    """
    Get a given regulator from database
    """
    return mapi.get_object(Regulator, **kwargs)


def get_regulator_by_id(protrend_id: str) -> Regulator:
    """
    Get a given regulator from database using the protrend identifier
    """
    return mapi.get_object(Regulator, protrend_id=protrend_id)


def get_last_regulator() -> Regulator:
    """
    Get the last regulator from database using the protrend identifier
    """
    return mapi.get_last_object(Regulator, 'protrend_id')
