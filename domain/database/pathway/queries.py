from typing import List

from data import Pathway
import domain.model_api as mapi


def get_pathways() -> List[Pathway]:
    """
    Get pathways list from database
    """
    return mapi.get_objects(Pathway)


def filter_pathways(*args, **kwargs) -> List[Pathway]:
    """
    Get and filter pathways from database
    """
    return mapi.filter_objects(Pathway, *args, **kwargs)


def order_by_pathways(*fields) -> List[Pathway]:
    """
    Get and order by pathways from database
    """
    return mapi.order_by_objects(Pathway, *fields)


def order_pathways_by_id() -> List[Pathway]:
    """
    Get and order by pathways by protrend identifier from database
    """
    return mapi.order_by_objects(Pathway, 'protrend_id')


def get_pathway(**kwargs) -> Pathway:
    """
    Get a given pathway from database
    """
    return mapi.get_object(Pathway, **kwargs)


def get_pathway_by_id(protrend_id: str) -> Pathway:
    """
    Get a given pathway from database using the protrend identifier
    """
    return mapi.get_object(Pathway, protrend_id=protrend_id)


def get_last_pathway() -> Pathway:
    """
    Get the last pathway from database using the protrend identifier
    """
    return mapi.get_last_object(Pathway, 'protrend_id')