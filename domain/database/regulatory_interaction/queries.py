from typing import List

from data import RegulatoryInteraction
import domain.model_api as mapi


def get_interactions() -> List[RegulatoryInteraction]:
    """
    Get interactions list from database
    """
    return mapi.get_objects(RegulatoryInteraction)


def filter_interactions(*args, **kwargs) -> List[RegulatoryInteraction]:
    """
    Get and filter interactions from database
    """
    return mapi.filter_objects(RegulatoryInteraction, *args, **kwargs)


def order_by_interactions(*fields) -> List[RegulatoryInteraction]:
    """
    Get and order by interactions from database
    """
    return mapi.order_by_objects(RegulatoryInteraction, *fields)


def order_interactions_by_id() -> List[RegulatoryInteraction]:
    """
    Get and order by interactions by protrend identifier from database
    """
    return mapi.order_by_objects(RegulatoryInteraction, 'protrend_id')


def get_interaction(**kwargs) -> RegulatoryInteraction:
    """
    Get a given interaction from database
    """
    return mapi.get_object(RegulatoryInteraction, **kwargs)


def get_interaction_by_id(protrend_id: str) -> RegulatoryInteraction:
    """
    Get a given interaction from database using the protrend identifier
    """
    return mapi.get_object(RegulatoryInteraction, protrend_id=protrend_id)


def get_last_interaction() -> RegulatoryInteraction:
    """
    Get the last interaction from database using the protrend identifier
    """
    return mapi.get_last_object(RegulatoryInteraction, 'protrend_id')
