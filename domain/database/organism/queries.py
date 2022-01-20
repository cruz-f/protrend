from typing import List

from data import Organism
import domain.model_api as mapi


def get_organisms() -> List[Organism]:
    """
    Get organisms list from database
    """
    return mapi.get_objects(Organism)


def filter_organisms(*args, **kwargs) -> List[Organism]:
    """
    Get and filter organisms from database
    """
    return mapi.filter_objects(Organism, *args, **kwargs)


def order_by_organisms(*fields) -> List[Organism]:
    """
    Get and order by organisms from database
    """
    return mapi.order_by_objects(Organism, *fields)


def order_organisms_by_id() -> List[Organism]:
    """
    Get and order by organisms by protrend identifier from database
    """
    return mapi.order_by_objects(Organism, 'protrend_id')


def get_organism(**kwargs) -> Organism:
    """
    Get a given organism from database
    """
    return mapi.get_object(Organism, **kwargs)


def get_organism_by_id(protrend_id: str) -> Organism:
    """
    Get a given organism from database using the protrend identifier
    """
    return mapi.get_object(Organism, protrend_id=protrend_id)


def get_last_organism() -> Organism:
    """
    Get the last organism from database using the protrend identifier
    """
    return mapi.get_last_object(Organism, 'protrend_id')
